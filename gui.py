'''
Graafinen klusterointityökalun pääohjelma.
Ilpo Kantonen ilpo@iki.fi. Started spring 2018. AI assisted automn 2025
'''

import sys, csv, os.path

from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QPushButton, QTextEdit, QLabel) # , QProgressBar
from PyQt6.QtCore import QThread, pyqtSignal, QObject

from kit import Kit
from cnetwork import Nclusters
from mtsettings import KITSFILE, HAPLOGROUP, OUTPUTDIR

class Worker(QObject):
    ''' Taustasäie, joka suorittaa aikaa vievän datan käsittelyn. '''
    finished, progress = pyqtSignal(), pyqtSignal(str)
    n: Nclusters                            # Klusteriverskosto
    kits: list                              # Kittilista

    def __init__(self, n_clusters_instance):
        super().__init__()
        if n_clusters_instance is None:     # Käytä annettua Nclusters-instanssia jos sellainen oli annettu,
            self.n = Nclusters()
        else:                               # muuten luodaan uusi oletusinstanssi.
            self.n = n_clusters_instance
        self.kits = []

    def make_cluster_network(self):
        ''' Make Cluster network '''
        print("Tehdään klusteriverkko.")

    def run(self):
        ''' Käynnistää datan käsittelyn '''

        fname = HAPLOGROUP + '.json'
        if os.path.isfile(fname):
            # self.progress.emit(f"Haploryhmän {HAPLOGROUP} valmis klusteriverkosto löytyi.")
            self.n.load_from_json(fname)
            self.progress.emit(f"Haploryhmän {HAPLOGROUP} valmis klusteriverkosto ladattu.")
        else:
            self.progress.emit(f"Haploryhmän {HAPLOGROUP} valmista klusteriverkostoa ei ollut.")

        data = None

        with open(KITSFILE, newline='') as f:
            reader = csv.reader(f)
            data = [tuple(row) for row in reader]

        # print("data tyyppi =", type(data))

        found, notfound = "", ""

        # for i, row in enumerate(data):
        for i in range( len(data) ):
            k = Kit(data[i][0], data[i][1], data[i][2])
            self.kits.append(k)
            if os.path.isfile(k.file):          # Löytyykö kitin osumalistatiedosto?
                found += f' {k.id}'
                k.read_matches()                # Käydään kitin osumat läpi ja lisätään 4-tasoiseen osumalistaan.
            else:
                notfound += f' {k.id}'

        found, notfound = found.strip(), notfound.strip()

        match len(found.split()):
            case 0:
                match len(notfound.split()):
                    case 0: self.progress.emit("#Yhtään kittiä ei löytynyt.")
                    case 1: self.progress.emit(f"Kitin {notfound} osumalistaa ei löytynyt.")
                    case _: self.progress.emit(f"Kittien {notfound} osumalistoja ei löytynyt.")
            case 1:
                match len(notfound.split()):
                    case 0: self.progress.emit(f"Luettiin kitin {found} osumalistat.")
                    case 1: self.progress.emit(f"Luettiin kitin {found} osumalistat. Kitin {notfound} osumalistoja ei löytynyt.")
                    case _: self.progress.emit(f"Luettiin kitin {found} osumalistat. Kittien {notfound} osumalistoja ei löytynyt.")
            case _: self.progress.emit(f"Luettiin kittien {found} osumalistat. Kittien {notfound} osumalistoja ei löytynyt.")

        self.progress.emit("Tähän asti ohjelma toiminee ok. ***************************")

        for k in self.kits:
            self.n.add_kit(k)  # for z in k.gds: self.n.add(z)
        self.progress.emit("Kittien mahdolliset lisäosumat lisätty klusteriverkostoon.")

        self.progress.emit("Poistetaan duplikaattiklusterit...")
        dint = 0
        while self.n.delete_duplicates():
            dint += 1
        if dint:
            self.progress.emit(f'Poistettiin {dint} duplikaattiklusteria.')

        self.progress.emit("Jaetaan epäyhtenäisiä klustereita...")
        sint = 0
        while self.n.split_clusters():
            sint += 1
        if sint:
            self.progress.emit(f'Jaettiin {sint} klusteria.')

        self.progress.emit("Valmis! Voit nyt suorittaa toimintoja.")

        # self.n.write(OUTPUTDIR + HAPLOGROUP + ".json")   # Lopuksi talletetaan oleamssa oleva klusteriverkosto

        self.finished.emit()


class MainWindow(QMainWindow):
    ''' Graafisen käyttöliittymän pääikkuna. Sisältää tekstialueen ja painikkeet toimintoihin '''
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"mtDNA Klusterianalyysi")
        self.setGeometry(100, 100, 600, 500)

        self.n = Nclusters()

        # Keskuswidget ja layout
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

        # Loki-ikkuna tulosteille
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        # self.log_output.setText("Käynnistetään...")
        self.layout.addWidget(self.log_output)

        # Asetetaan Nclusters-instanssi käyttämään GUI:n lokia
        # self.n.set_logger(self.log_message)

        # Painikkeet
        self.buttons = {
            "Näytä klusteriverkosto": self.n.show,
            "Luo tiedostot Gephille / Pyplotille": self.n.gephi,
            "Tulosta klusterit": self.n.show, # Sama kuin ensimmäinen
            "Vie klusterit XML/JSON-muotoon": self.n.mk_xml,
            "Näytä MDKA:t": self.n.show_mdkas,
            "Talleta ja lopeta": self.save_and_exit,
        }

        self.button_widgets = []
        for text, func in self.buttons.items():
            button = QPushButton(text)
            button.clicked.connect(func)
            button.setEnabled(False) # Deaktivoidaan aluksi
            self.layout.addWidget(button)
            self.button_widgets.append(button)

        self.save_exit_button = QPushButton("Tallenna ja poistu")
        self.save_exit_button.clicked.connect(self.save_and_exit)
        self.save_exit_button.setEnabled(False)
        self.layout.addWidget(self.save_exit_button)

        # Käynnistetään datan lataus taustalla
        # self.read_kits()
        self.start_data_processing()

    # def start_data_processing(self):
    def save_and_exit(self):
        ''' Save and exit '''
        if self.n is not None:
            try:
                filename = os.path.join(OUTPUTDIR, HAPLOGROUP + '.json')
                self.n.write(filename)
                self.log_message(f"Tiedot tallennettu onnistuneesti tiedostoon {filename}.")
            except Exception as e:
                self.log_message(f"Virhe tallennuksessa: {e}")
        self.log_message("Suljetaan ohjelma...")
        QApplication.instance().quit()

    def log_message(self, message):
        """Lisää viestin GUI:n tekstikenttään."""
        self.log_output.append(message)
        # Vieritetään automaattisesti alas
        self.log_output.verticalScrollBar().setValue(self.log_output.verticalScrollBar().maximum())

    def start_data_processing(self):
        """Luo ja käynnistää taustasäikeen."""
        self.thread = QThread()
        self.worker = Worker(self.n)
        self.worker.moveToThread(self.thread)

        # Yhdistetään signaalit
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(self.log_message)
        self.worker.finished.connect(self.on_loading_finished)

        self.thread.start()
        # self.log_message("Aloitetaan osumalistojen luku taustalla...")
        # Lue kits.csv -tiedostosta kitit.


    def on_loading_finished(self):
        """Aktivoi painikkeet, kun datan käsittely on valmis."""
        for button in self.button_widgets:
            button.setEnabled(True)
        self.save_exit_button.setEnabled(True)

    def save_and_exit(self):
        ''' Save and exit '''
        if self.n is not None:
            try:
                filename = OUTPUTDIR + HAPLOGROUP + '.json'
                self.n.write(filename)
                # https://stackoverflow.com/questions/52900086/write-specific-json-structure-to-json-file-in-python
                self.log_message(f"Tiedot tallennettu onnistuneesti tiedostoon {filename}.")
            except IOError as e:
                self.log_message(f"Virhe tallennuksessa: {e}")
        self.log_message("Suljetaan ohjelma...")
        QApplication.instance().quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')                  # KDE-tyyliä varten voi käyttää "Fusion" tai "Breeze"

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
