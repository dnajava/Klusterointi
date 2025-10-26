
"""
Graafinen klusterointityökalun pääohjelma.
Ilpo Kantonen ilpo@iki.fi. Started spring 2018. AI assisted autumn 2025
"""

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QPushButton, QTextEdit, QLabel, QDialog
)
from PyQt6.QtCore import QThread, pyqtSignal, QObject, Qt

import sys, csv, os, json
import networkx as nx
import matplotlib.pyplot as plt

# Paikalliset moduulit (oletetaan, että ovat samassa projektissa)
from kit import Kit
from netcluster import NetCluster
from netclusters import NetClusters
from mtsettings import KITSFILE, HAPLOGROUP, OUTPUTDIR

# Oletusmerkistö JSON-tallennukseen
DEFAULT_ENCODING = 'utf-8'


class Worker(QObject):
    """Taustasäie, joka suorittaa aikaa vievän datan käsittelyn."""
    # Signaalit (luokka-attribuuttina)
    finished = pyqtSignal()
    progress = pyqtSignal(str)
    plot_data_ready = pyqtSignal(object, object, object, object)  # (B, pos, colors, title)

    def __init__(self, n_clusters_instance: NetClusters = None):
        super().__init__()
        # n on NetClusters-instanssi (verkko + klusterit)
        self.n = n_clusters_instance if n_clusters_instance is not None else NetClusters()
        self.kits = []
        self.alreadynet = False

    def load_kitlist(self):
        """Lataa kitit levyltä ja lukee niiden osumatiedostot."""
        self.kits.clear()

        try:
            with open(KITSFILE, newline='') as f:
                reader = csv.reader(f)
                data = [tuple(row) for row in reader]
        except FileNotFoundError:
            self.progress.emit(f"Virhe: {KITSFILE} ei löytynyt.")
            self.finished.emit()
            return

        found, notfound = [], []

        for row in data:
            # oletetaan, että rivillä on vähintään 3 saraketta (id, nimi, tiedosto)
            k = Kit(*row[:3])
            self.kits.append(k)
            if os.path.isfile(k.file):
                found.append(k.id)
                try:
                    k.read_matches()
                except Exception as e:
                    self.progress.emit(f"Varoitus: virhe luettaessa {k.file}: {e}")
            else:
                notfound.append(k.id)

        # Muodosta viesti käyttöliittymään
        if not found and not notfound:
            msg = "Yhtään kittiä ei löytynyt."
        elif notfound and not found:
            msg = f"Kittien {', '.join(notfound)} osumalistoja ei löytynyt."
        elif found and not notfound:
            msg = f"Luettiin {len(found)} kitin osumalistat: {', '.join(found)}"
        else:
            msg = (
                f"Luettiin {len(found)} kitin osumalistat ({', '.join(found)}). "
                f"{len(notfound)} kitin osumalistoja ei löytynyt ({', '.join(notfound)})."
            )

        self.progress.emit(msg)
        self.finished.emit()

    def load_from_json(self, filename: str):
        """Lataa verkko- / klusteritiedot JSON-tiedostosta."""
        try:
            with open(filename, "r", encoding=DEFAULT_ENCODING) as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            self.progress.emit(f"Virhe JSON-latauksessa: {e}")
            return

        # Olettaen, että NetClusters:llä on attribuutti nclusters johon data asetetaan
        if isinstance(data, dict) and "nclusters" in data:
            self.n.nclusters = data["nclusters"]
        else:
            self.n.nclusters = data

        self.progress.emit(f"Ladattiin klusteriverkosto tiedostosta {filename}.")

    def show_network(self):
        """Lähettää verkon piirtodataa pääsäikeelle; yksinkertainen versio."""
        # Käytetään self.n.nclusters - oletus on list of clusters tai sopiva rakenne
        clusters = getattr(self.n, "nclusters", None)
        if not clusters:
            self.progress.emit("Klusteriverkko on tyhjä — ei piirrettävää.")
            self.finished.emit()
            return

        # Muodostetaan yksinkertainen bipartite-tyyppinen graafi: klusteri-nodet ja jäsen-nodet
        B = nx.Graph()
        for i, clu in enumerate(clusters, start=1):
            cname = f"Klusteri {i}"
            B.add_node(cname, type='hyperedge')
            # Oletetaan, että 'clu' on iteroitava jäsenten listaksi
            for member in clu:
                # member voi olla esim. tuple; käytetään member[0] jos tuple, muuten str(member)
                mlabel = member if isinstance(member, str) else (member[0] if isinstance(member, (list, tuple)) else str(member))
                B.add_node(mlabel, type='node')
                B.add_edge(cname, mlabel)

        pos = nx.spring_layout(B, seed=42)
        colors = ['red' if B.nodes[n].get('type') == 'hyperedge' else 'skyblue' for n in B.nodes]
        title = f"Haploryhmän {HAPLOGROUP} klusteriverkosto"

        self.plot_data_ready.emit(B, pos, colors, title)
        self.progress.emit("Klusteriverkon data valmis.")
        self.finished.emit()

    def show_mdkas(self):
        """Avaa uuden ikkunan ja näyttää klusterit tekstimuodossa."""
        # Tämä metodi ajetaan taustasäikeestä -> emme luo GUI-ikkunoita täällä.
        # Sen sijaan muodostetaan raportti ja lähetetään progress-signaalina.
        clusters = getattr(self.n, "nclusters", None)
        report_lines = []
        MDKATAB = "    "
        if not clusters:
            report_lines.append("Cluster network is empty.")
        else:
            known_mdkas = 0
            unknown_mdkas = 0
            for i, clu in enumerate(clusters, start=1):
                report_lines.append(f"Klusteri {i}:")
                # Jos klusterissa on elementtejä, olettakaamme match[6] sisältää MDKA:n nimen
                for match in clu:
                    # käsitellään match turvallisesti
                    name = ''
                    try:
                        name = match[6] if len(match) > 6 else ''
                    except Exception:
                        name = ''
                    if not name:
                        unknown_mdkas += 1
                        report_lines.append(f"{MDKATAB}<tuntematon MDKA>")
                    else:
                        known_mdkas += 1
                        report_lines.append(f"{MDKATAB}{name}")
                # rajataan esitystä (sama logiikka kuin alkuperäisessä)
                if i >= 10:
                    report_lines.append(f"{MDKATAB}... (näytetty 10 ensimmäistä klusteria)")
                    break

            report_lines.append(f"Yhteensä on {known_mdkas} MDKA:ta ja {unknown_mdkas} tuntematonta MDKA:ta.")

        # Lähetetään valmis raportti progress-signaalina (monirivinen teksti)
        self.progress.emit("\n".join(report_lines))
        self.finished.emit()

    def run(self):
        """Esimerkkiajo: Lataa klusteriverkoston jos löytyy."""
        fname = f"{HAPLOGROUP}.json"
        if os.path.isfile(fname):
            self.alreadynet = True
            self.load_from_json(fname)
            self.progress.emit(f"Haploryhmän {HAPLOGROUP} valmis klusteriverkosto ladattu.")
        else:
            self.progress.emit(f"Haploryhmän {HAPLOGROUP} klusteriverkostoa ei löytynyt.")

        self.finished.emit()

    def make_cluster_network(self):
        """Paikallinen rakentaja (placeholder)."""
        # Tämä voisi rakentaa self.n:n klusterit käyttämällä self.kits jne.
        self.progress.emit("Tehdään klusteriverkko (placeholder).")
        # Simuloidaan valmis
        self.finished.emit()

    def write(self, fname_p=None):
        """Tallenna JSON-muotoon. Jos ei parametria, tallenna oletuspolkuun OUTPUTDIR/HAPLOGROUP.json"""
        if fname_p is None:
            fname_p = os.path.join(OUTPUTDIR, f"{HAPLOGROUP}.json")
        try:
            with open(fname_p, 'w', encoding=DEFAULT_ENCODING) as f:
                # Pyydetään että NetClusters tarjoaa seralisoitavan rakenteen self.n.nclusters
                json.dump(getattr(self.n, "nclusters", {}), f, indent=2, ensure_ascii=False)
            self.progress.emit(f"Tallennettu {fname_p}")
        except Exception as e:
            self.progress.emit(f"Virhe tallennuksessa: {e}")

    def autosave(self):
        """Tallentaa verkon automaattisesti JSON-tiedostoon."""
        try:
            os.makedirs(OUTPUTDIR, exist_ok=True)
            filename = os.path.join(OUTPUTDIR, f"{HAPLOGROUP}.json")
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(getattr(self.n, "nclusters", {}), f, indent=2, ensure_ascii=False)
            self.progress.emit(f"Automaattinen tallennus suoritettu: {filename}")
        except Exception as e:
            self.progress.emit(f"Automaattinen tallennus epäonnistui: {e}")


class MainWindow(QMainWindow):
    """Graafisen käyttöliittymän pääikkuna."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("mtDNA Klusterianalyysi")
        self.setGeometry(100, 100, 800, 600)

        # Alusta NetClusters-objekti (käytetään mm. Workerille)
        self.n = NetClusters()

        # Ei luoda säiettä heti väärin — käytetään start_worker:ia käynnistyksissä
        self.thread = None
        self.worker = None

        # GUI
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Otsikko
        self.title_label = QLabel(f"Haploryhmä {HAPLOGROUP}")
        font = self.title_label.font()
        font.setPointSize(14)
        font.setBold(True)
        self.title_label.setFont(font)
        self.layout.addWidget(self.title_label)

        # Loki-ikkuna
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.layout.addWidget(self.log_output)

        # Painikkeet
        self.add_button("Lataa klusteriverkosto", self.start_load_network)
        self.add_button("Lataa kitit", self.start_load_kits)
        self.add_button("Näytä klusteriverkko", self.start_show_network)
        self.add_button("Näytä MDKAt", self.start_show_mdkas)

        # Tallenna ja poistu
        self.save_exit_button = QPushButton("Talleta ja poistu")
        self.save_exit_button.clicked.connect(self.save_and_exit)
        self.layout.addWidget(self.save_exit_button)

    def add_button(self, text, func):
        button = QPushButton(text)
        button.clicked.connect(func)
        self.layout.addWidget(button)

    # -------------------------
    # Taustasäikeen käynnistykset
    # -------------------------
    def start_load_network(self):
        self.start_worker(mode="network")

    def start_show_network(self):
        self.start_worker(mode="shownetwork")

    def start_show_mdkas(self):
        self.start_worker(mode="showmdkas")

    def start_load_kits(self):
        self.start_worker(mode="kits")

    def start_worker(self, mode="network"):
        """Yhteinen metodi säikeen käynnistämiseen."""
        # Luo uusi säie + worker tähän tehtävään
        thread = QThread()
        worker = Worker(self.n)

        worker.moveToThread(thread)

        # Liitetään oikea metodi thread.started:iin
        if mode == "network":
            thread.started.connect(worker.run)
        elif mode == "kits":
            thread.started.connect(worker.load_kitlist)
        elif mode == "shownetwork":
            thread.started.connect(worker.show_network)
        elif mode == "showmdkas":
            thread.started.connect(worker.show_mdkas)
        else:
            thread.started.connect(worker.run)

        # Signaalit
        worker.progress.connect(self.log_message)
        worker.plot_data_ready.connect(self.update_plot)
        worker.finished.connect(thread.quit)
        worker.finished.connect(worker.deleteLater)
        thread.finished.connect(thread.deleteLater)

        # Käytetään paikallisia viitteitä estääksemme tuhoutumisen ennen aikojaan
        self.thread = thread
        self.worker = worker

        thread.start()
        self.log_message(f"Aloitetaan {'kittien' if mode=='kits' else 'verkoston'} lataus...")

    def update_plot(self, B, pos, colors, title):
        plt.figure(figsize=(12, 8))
        nx.draw(B, pos, with_labels=True, node_color=colors, node_size=800, font_weight='bold')
        plt.title(title)
        plt.show()

    def on_progress(self, msg):
        print(msg)

    def on_finished(self):
        print("Työ valmis.")

    # -------------------------
    # GUI:n toiminnot
    # -------------------------
    def log_message(self, message):
        """Tulostaa viestin loki-ikkunaan."""
        # message voi olla myös lista tai muu; muotoillaan str:ksi
        if isinstance(message, (list, tuple)):
            message = "\n".join(map(str, message))
        self.log_output.append(str(message))
        self.log_output.verticalScrollBar().setValue(self.log_output.verticalScrollBar().maximum())

    def save_and_exit(self):
        """Talleta JSON ja poistu."""
        try:
            filename = os.path.join(OUTPUTDIR, f"{HAPLOGROUP}.json")
            # Käytetään self.worker:n writeä jos se on olemassa, muuten self.n:ää
            if self.worker is not None:
                try:
                    # Worker.write tallentaa self.n.nclusters
                    self.worker.write(filename)
                except Exception:
                    # fallback: yritä kutsua NetClusters:n write-menetelmää
                    if hasattr(self.n, 'write'):
                        self.n.write(filename)
                    else:
                        # kirjoitetaan nclusters suoraan
                        with open(filename, 'w', encoding=DEFAULT_ENCODING) as f:
                            json.dump(getattr(self.n, "nclusters", {}), f, indent=2, ensure_ascii=False)
            else:
                with open(filename, 'w', encoding=DEFAULT_ENCODING) as f:
                    json.dump(getattr(self.n, "nclusters", {}), f, indent=2, ensure_ascii=False)

            self.log_message(f"Tiedot tallennettu tiedostoon {filename}.")
        except Exception as e:
            self.log_message(f"Virhe tallennuksessa: {e}")
        self.log_message("Suljetaan ohjelma...")
        QApplication.instance().quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    try:
        app.setStyle('Fusion')
    except Exception:
        # Jos tyyliä ei löydy, ei kaadu
        pass

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


'''
Kutsu autosave() seuraavissa kohdissa

Lisää rivin self.autosave() seuraaviin metodeihin:

1️⃣ load_from_json() loppuun:
        self.progress.emit(f"Ladattiin klusteriverkosto tiedostosta {filename}.")
        self.autosave()  # <-- lisätty

2️⃣ make_cluster_network() loppuun:
        self.progress.emit("Tehdään klusteriverkko (placeholder).")
        self.autosave()  # <-- lisätty
        self.finished.emit()

3️⃣ load_kitlist() loppuun (jos kittejä luettu):
        self.progress.emit(msg)
        self.autosave()  # <-- lisätty
        self.finished.emit()

🧠 Lisävinkki

Jos haluat vielä varmistaa, että automaattitallennus ei käynnisty liian usein (esim. jos klusteriverkkoa rakennetaan vaiheittain), voit lisätä pienen “debounce”-logiikan:

import time

class Worker(QObject):
    ...
    _last_save_time = 0

    def autosave(self):
        """Tallentaa verkon, mutta enintään kerran 10 sekunnissa."""
        now = time.time()
        if now - self._last_save_time < 10:
            return
        self._last_save_time = now
        ...

✅ Lopputulos

Nyt ohjelma tallentaa automaattisesti OUTPUTDIR/HAPLOGROUP.json-tiedoston aina kun:

verkko ladataan,

uusia kittejä luetaan,

tai klusteriverkko rakennetaan uudelleen.

Ja käyttäjä näkee viestin loki-ikkunassa:

Automaattinen tallennus suoritettu: data/mtHaplo.json

'''