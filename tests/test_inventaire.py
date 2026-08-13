import os
import sys
import unittest

sys.path.insert(0, '.')

from teranganet.inventaire import charger_inventaire, trouver_equipement


class TestChargerInventaire(unittest.TestCase):

    def setUp(self):
        self.chemin_yaml_casse = "tests/yaml_casse.yaml"
        with open(self.chemin_yaml_casse, "w", encoding="utf-8") as f:
            f.write("sites: [code: DKR")  # YAML volontairement mal formé

    def tearDown(self):
        if os.path.exists(self.chemin_yaml_casse):
            os.remove(self.chemin_yaml_casse)

    def test_nombre_equipements_et_sites(self):
        sites, equipements = charger_inventaire("data/equipements.yaml")
        self.assertEqual(len(sites), 3)
        self.assertEqual(len(equipements), 6)

    def test_attributs_equipement(self):
        sites, equipements = charger_inventaire("data/equipements.yaml")
        equipement = trouver_equipement("ANT1-DKR", equipements)
        self.assertEqual(equipement.type, "antenne")
        self.assertEqual(equipement.ip, "10.10.1.10")
        self.assertEqual(equipement.statut, "en service")
        self.assertEqual(equipement.site.code, "DKR")

    def test_equipement_inconnu(self):
        sites, equipements = charger_inventaire("data/equipements.yaml")
        equipement = trouver_equipement("INCONNU", equipements)
        self.assertIsNone(equipement)

    def test_fichier_inexistant(self):
        sites, equipements = charger_inventaire("data/fichier_qui_nexiste_pas.yaml")
        self.assertIsNone(sites)
        self.assertIsNone(equipements)

    def test_yaml_malforme(self):
        sites, equipements = charger_inventaire(self.chemin_yaml_casse)
        self.assertIsNone(sites)
        self.assertIsNone(equipements)


if __name__ == "__main__":
    unittest.main()