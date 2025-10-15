''' Nclusters '''
import time
class NclustersTemp:
    '''
    Network of mt-dna GD clusters. Tools to add nodes, find and delete
    duplicate clusters, split cluster. Export to txt, xml or spreadsheet.
    And make nodes.csv and links.csv to Gephi.
    '''

    def __init__(self):
        ''' Konstruktori '''
        self._clusters = []
        self._log_callback = print # Oletusarvoisesti tulostaa konsoliin

    def set_logger(self, callback_func):
        """Asetetaan funktio, jota käytetään lokiviestien näyttämiseen GUI:ssa."""
        self._log_callback = callback_func

    def _log(self, message):
        ''' Write a log line '''
        self._log_callback(message)
    def add(self, cluster):
        ''' Add a cluster to network of clusters '''
        self._clusters.append(cluster)

    def read(self, fname):
        ''' Read already exist network of clusters from disk '''
        self._log(f"Luetaan valmis verkosto tiedostosta {fname}...")
        # self._clusters = [["Esimerkkiklusteri 1"], ["Esimerkkiklusteri 2"]]

        print(f"Reading file: {file_path}")

        read_obj = None
        FENCODING="utf-8"
        try:
            with open(fname, 'r', encoding=FENCODING) as read_obj:
                csv_reader = reader(read_obj)
                for ind, m in enumerate(csv_reader):
                    # Read actual match line
                    new_match = FileMatch(
                        kit_id,
                        int(m[0]),
                        m[1], m[2], m[3], m[4], m[5], m[6]
                    )
                    self.gds.add(int(m[0]), new_match)
        except (IOError, OSError) as err:
            print(f"Error reading {file_path}: {err}")
        finally:
            if read_obj is not None:
                read_obj.close()


    def write(self, fname):
        self._log(f"Tallennetaan verkosto tiedostoon {fname}...")
        print(f"Tallennetaan verkosto tiedostoon {fname}...")
        time.sleep(1) # Simuloidaan tallennusta

    def delete_duplicates(self):
        self._log("Poistetaan duplikaatteja...")
        time.sleep(0.5)
        # Palautetaan False, jotta silmukka suoritetaan vain kerran esimerkissämme
        return False

    def split_clusters(self):
        ''' Split clusters iw necessary '''
        self._log("Jaetaan epäyhtenäisiä klustereita...")
        time.sleep(0.5)
        return False

    def show(self):
        ''' Show network of clusters'''
        self._log("\n--- Klusteriverkosto ---")
        if not self._clusters:
            self._log("Verkosto on tyhjä.")
            return
        for i, cluster in enumerate(self._clusters[:5]): # Näytetään max 5
            self._log(f"Klusteri {i+1}: {', '.join(cluster)}")
        if len(self._clusters) > 5:
            self._log(f"... ja {len(self._clusters) - 5} muuta klusteria.")
        self._log("------------------------\n")

    def gephi(self):
        ''' Make a file of clusters and their mdkas for Gephi '''
        self._log("\nLuodaan nodes.csv ja links.csv Gephiä varten...")
        time.sleep(1)
        self._log("Tiedostot luotu onnistuneesti.\n")

    def mk_xml(self):
        ''' Make a XML file from network of clusters '''
        self._log("\nMuodostetaan klustereista XML-tiedosto...")
        time.sleep(1)
        self._log("XML-tiedosto luotu onnistuneesti.\n")

    def show_mdkas(self):
        ''' Show mdkas from network of clusters '''
        self._log("\n--- MDKA:t (Most Distant Known Ancestors) ---")
        self._log("MDKA 1: Esi-isä A, 1750")
        self._log("MDKA 2: Esi-isä B, 1820")
        self._log("----------------------------------------------\n")
