'''
Päivitetty osumien lukumetodi on huomattavasti vankempi, sillä se etsii sarakkeet niiden nimien
(Full Name ja Genetic Distance) perusteella, eikä oletettujen sarakeindeksien (kuten row[0] ja row[6]) mukaan.
Tämä tarkoittaa, että koodi toimii, vaikka CSV-tiedostoon lisättäisiin sarakkeita tai niiden järjestystä muutettaisiin.
'''

import pandas as pd
from mtsettings import DLDIR, HAPLOGROUP, FENCODING
from gds import Gds


class Kit:
    id: str
    kit_name: str
    haplogroup: str
    file: str
    gds: Gds

    def __init__(self, id_p: str, name_p: str, day_p: str, haplogroup_p: str=None):
        self.id = id_p
        self.kit_name = name_p
        self.haplogroup = HAPLOGROUP if haplogroup_p is None else haplogroup_p
        self.file = DLDIR + id_p + '_MT_DNA_Matches_' + day_p + '.csv' # Matchlist filename
        self.gds = Gds()    # Steps 0 (exact match), 1, 2, 3
        # self.read_kit_clusters(self.id, self.name, self.file)       # Read match clusters

        # Listat sisältävät edelleen sanakirjoja (dict)
        self.gd0 = []  # Tasan (Exact Match)
        self.gd1 = []  # 1 step
        self.gd2 = []  # 2 steps
        self.gd3 = []  # 3 steps

    def show(self):
        print(f"Kit id={self.id} kit_name={self.kit_name} haplogroup={self.haplogroup} file={self.file}")

    def read(self):
        """
        Lukee matchit annetusta tiedostopolusta (file_path) Pandas DataFrameen.
        Jäsentää jokaisen osuman (rivin) sanakirjaksi ja tallentaa sen
        oikeaan listaan (gd0, gd1, gd2, gd3) geneettisen etäisyyden
        (Genetic Distance) perusteella.
        """
        try:
            df = pd.read_csv(self.file, delimiter=',', skipinitialspace=True, encoding=FENCODING)
        except UnicodeDecodeError:
            try:
                df = pd.read_csv(self.file, delimiter=',', skipinitialspace=True, encoding='latin-1')
            except Exception as e:
                print(f"Virhe luettaessa tiedostoa (latin-1): {e}")
                return
        except FileNotFoundError:
            print(f"Virhe: Tiedostoa ei löydy polusta: {self.file}")
            return
        except pd.errors.EmptyDataError:
            print(f"Virhe: CSV-tiedosto on tyhjä: {self.file}")
            return
        except Exception as e:
            print(f"Yleinen virhe luettaessa CSV-tiedostoa: {e}")
            return

        # --- Datan käsittely ---
        # Tämä osa on identtinen edellisen version kanssa
        try:
            df.columns = df.columns.str.strip()
            name_col = 'Full Name'
            gd_col = 'Genetic Distance'

            if gd_col not in df.columns:
                print(f"Virhe: CSV-tiedostosta puuttuu pakollinen sarake '{gd_col}'.")
                return

            # Iteroi DataFramen rivit läpi
            for index, row in df.iterrows():

                # Muunna koko rivi sanakirjaksi
                match_data = row.to_dict()

                # Siivoa sanakirjan arvot
                cleaned_data = {}
                for key, value in match_data.items():
                    if pd.isna(value):
                        cleaned_data[key] = ""  # Muuta tyhjäksi merkkijonoksi
                    elif isinstance(value, str):
                        cleaned_data[key] = value.strip()
                    else:
                        cleaned_data[key] = value

                # Hae siivottu GD-arvo lajittelua varten
                gd_cleaned = cleaned_data.get(gd_col, "")

                # Sijoita koko siivottu sanakirja oikeaan listaan
                if gd_cleaned == "Exact Match":
                    self.gd0.append(cleaned_data)
                elif gd_cleaned == "1 step":
                    self.gd1.append(cleaned_data)
                elif gd_cleaned == "2 steps":
                    self.gd2.append(cleaned_data)
                elif gd_cleaned == "3 steps":
                    self.gd3.append(cleaned_data)

        except Exception as e:
            print(f"Virhe käsiteltäessä CSV-dataa Pandasilla: {e}")

    def has_match(self, name: str):
        """
        Tarkistaa, löytyykö annettua nimeä (Full Name) mistään GD-listasta.
        """
        search_name = name.strip()

        for gd_list in [self.gd0, self.gd1, self.gd2, self.gd3]:
            for match_data in gd_list:
                if match_data.get('Full Name') == search_name:
                    return True
        return False

    def __str__(self):
        """
        Palauttaa merkkijonoesityksen kitistä ja osumien määristä.
        """
        return "%s: %s, %s, %s, %s" % (self.kit_name, len(self.gd0), len(self.gd1), len(self.gd2), len(self.gd3))