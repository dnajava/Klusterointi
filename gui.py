'''
Graafinen klusterointityökalun pääohjelma.
Ilpo Kantonen ilpo@iki.fi. Started spring 2018. AI assisted automn 2025
'''

import sys
import os.path

from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QPushButton, QTextEdit, QLabel) # , QProgressBar
from PyQt6.QtCore import QThread, pyqtSignal, QObject

from kit import Kit
from cnetwork import Nclusters
from mtsettings import DLDIR, HAPLOGROUP, OUTPUTDIR


class Worker(QObject):
    '''
    Taustasäie, joka suorittaa aikaa vievän datan käsittelyn.
    '''

    finished = pyqtSignal()
    progress = pyqtSignal(str)
    n: list
    def __init__(self, n_clusters_instance):
        super().__init__()
        self.n = Nclusters()    # Create empty network of clusters

    def make_cluster_network(self):
        ''' Make Cluster network '''
        print("Tehdään klusteriverkko.")

    def run(self):
        ''' Käynnistää datan käsittelyn '''

        kits = []

        fname = HAPLOGROUP + '.json'
        if os.path.isfile(fname):
            self.progress.emit(f"Haploryhmän {HAPLOGROUP} valmis klusteriverkosto löytyi.")

            # print(f"fname={fname}")
            self.n = Nclusters.read(HAPLOGROUP)
            # TODO: Check if there are new match lists which are not in network
            self.n.show()
            self.progress.emit("Valmis klusteriverkosto ladattu.")

            self.progress.emit("Tarkista, ettei koneella ole uusia osumalistoja olemassaolevan klusteriverkoston lisäksi.")
        else:
            self.progress.emit(f"Haploryhmän {HAPLOGROUP} valmista klusteriverkostoa ei ollut.")
            kit_ids_list = Kit.read_kitlist()
            found, notfound = "", ""
            # kits = []

            for k in kit_ids_list:
                pvm = k[2][0:2] + k[2][2:4] + '-' + k[2][4:6] + '-' + k[2][6:8]
                fname2 = DLDIR + f'{k[0]}_MT_DNA_Matches_{pvm}.csv'

                if os.path.isfile(fname2):          # Löytyykö kitin osumalistatiedosto?
                    found += f' {k[0]}'
                    k = Kit(k[0], k[1], fname2)
                    kits.append(k)
                    # Käydään kitin osumat läpi ja lisätään sen kitin 4-tasoiseen osumalistaan gd:n mukaan.

                    # new_match = Match(k[0], k[1], pvm, HAPLOGROUP)
                    # print("New match = ", new_match.Fullname)
                    # matches.append(new_match)
                else:
                    notfound += f' {k[0]}'

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

        self.progress.emit("Valmis! Voit nyt suorittaa toimintoja.")
        if self.n is None:
            print("selffi n on None.")
        else:
            print("Selffi n ei ole None.")
            self.n.show()
        self.n.show()

        self.progress.emit("Tehdään klustereista verkosto...")
        for k in kits:
            self.n.add_kit(k)  # for z in k.gds: self.n.add(z)
        self.progress.emit("Kittien osumat lisätty klusteriverkostoon.")

        self.progress.emit("Poistetaan duplikaatit...")
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

        self.n.write(OUTPUTDIR + HAPLOGROUP + '.json')   # Lopuksi talletetaan oleamssa oleva klusteriverkosto

        self.finished.emit()


class MainWindow(QMainWindow):
    ''' Graafisen käyttöliittymän pääikkuna. Sisältää tekstialueen ja painikkeet toimintoihin '''
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"mtDNA Klusterianalyysi - {HAPLOGROUP}")
        self.setGeometry(100, 100, 600, 500)

        self.n = Nclusters()

        # Keskuswidget ja layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Otsikko
        self.title_label = QLabel(f"Toiminnot haploryhmälle: {HAPLOGROUP}")
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
