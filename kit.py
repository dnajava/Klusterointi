'''
Kit of DNA tested person. It has matches. Mt-dna matches of 4 levels. Y-dna matches not implemented yet.
'''
from unittest import case

import pandas as pd
from mtsettings import DLDIR, HAPLOGROUP, FENCODING
from gds import Gds
import datetime

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
        self.gds = Gds() # Steps 0, 1, 2 and 3

        self.gd0 = [] # Exact Match
        self.gd1 = [] # 1 step
        self.gd2 = [] # 2 steps
        self.gd3 = [] # 3 steps

    def show(self):
        print(f"Kit id={self.id} kit_name={self.kit_name} haplogroup={self.haplogroup} file={self.file}")
        print(f"Matches GD 0")
        print(" ", self.gd0)           # for j in range(0, len(self.gds[i]):
        print(f"Matches GD 1")
        print(" ", self.gd1)           # for j in range(0, len(self.gds[i]):
        print(f"Matches GD 2")
        print(" ", self.gd2)           # for j in range(0, len(self.gds[i]):
        print(f"Matches GD 3")
        print(" ", self.gd3)           # for j in range(0, len(self.gds[i]):

    def read_matches(self):
        """
        Lukee matchit annetusta tiedostopolusta (file_path) Pandas DataFrameen.
        Jäsentää jokaisen osuman (rivin) sanakirjaksi ja tallentaa sen
        oikeaan listaan (gd0, gd1, gd2, gd3) geneettisen etäisyyden
        (Genetic Distance) perusteella.

        Päivitetty osumien lukumetodi on huomattavasti vankempi, sillä se etsii sarakkeet niiden nimien
        (Full Name ja Genetic Distance) perusteella, eikä oletettujen sarakeindeksien (kuten row[0] ja row[6]) mukaan.
        Tämä tarkoittaa, että koodi toimii, vaikka CSV-tiedostoon lisättäisiin sarakkeita tai niiden järjestystä
        muutettaisiin.
        """
        try:
            df = pd.read_csv(self.file, delimiter=',', skipinitialspace=True, encoding=FENCODING)
        except FileNotFoundError:
            # print(f"Virhe: Tiedostoa ei löydy polusta: {self.file}")
            return
        except pd.errors.EmptyDataError:
            print(f"Virhe: CSV-tiedosto on tyhjä: {self.file}")
            return
        except Exception as e:
            print(f"Yleinen virhe luettaessa CSV-tiedostoa: {e}")
            return

        try:                                                        # --- Datan käsittely ---
            df.columns = df.columns.str.strip()
            # name_col = 'Full Name'
            gd_col = 'Genetic Distance'

            if gd_col not in df.columns:
                print(f"Virhe: CSV-tiedostosta puuttuu pakollinen sarake '{gd_col}'.")
                return

            for index, row in df.iterrows():                        # Iteroi DataFramen rivit läpi
                match_data = row.to_dict()                          # Muunna koko rivi sanakirjaksi
                cleaned_data = {}                                   # Siivoa sanakirjan arvot
                for key, value in match_data.items():
                    if pd.isna(value):
                        cleaned_data[key] = ""                      # Muuta tyhjäksi merkkijonoksi
                    elif isinstance(value, str):
                        cleaned_data[key] = value.strip()
                    else:
                        cleaned_data[key] = value

                gd_cleaned = cleaned_data.get(gd_col, "")           # Hae siivottu GD-arvo lajittelua varten

                match gd_cleaned:                                   # Sijoita koko siivottu sanakirja oikeaan listaan
                    case "Exact Match": self.gd0.append(cleaned_data)
                    case "1 step":      self.gd1.append(cleaned_data)
                    case "2 steps":     self.gd2.append(cleaned_data)
                    case "3 steps":     self.gd3.append(cleaned_data)

        except Exception as e:
            print(f"Virhe käsiteltäessä CSV-dataa Pandalla: {e}")

    def get_gd_matches(self, gd_p) -> list:
        match gd_p:
            case "Exact Match": return self.gd0
            case "1 step": return self.gd1
            case "2 steps": return self.gd2
            case "3 steps": return self.gd3

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