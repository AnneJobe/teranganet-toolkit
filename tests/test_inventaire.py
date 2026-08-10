import sys
import unittest

sys.path.insert(0, '.')

from teranganet.inventaire import charger_inventaire, trouver_equipement


class TestChargerInventaire(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()