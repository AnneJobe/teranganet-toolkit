import sys
import unittest
import json
import os
import shutil

sys.path.insert(0, '.')

from teranganet.rapport import ecrire_rapport


class TestEcrireRapport(unittest.TestCase):

    def setUp(self):
        self.dossier_test = "tests/rapports_test"

    def tearDown(self):
        if os.path.exists(self.dossier_test):
            shutil.rmtree(self.dossier_test)

    def test_rapport_contient_les_cles_attendues(self):
        rapport = {
            "horodatage": "2026-08-13 16:35",
            "sites": [
                {
                    "site": {
                        "code": "DKR",
                        "nom": "Dakar",
                        "latitude": 14.6928,
                        "longitude": -17.4467,
                    },
                    "vent": 13.4,
                    "temperature": 30.9,
                    "alertes": [],
                }
            ],
        }

        chemin_fichier = ecrire_rapport(rapport, dossier=self.dossier_test)
        self.assertTrue(os.path.exists(chemin_fichier))

        with open(chemin_fichier, encoding="utf-8") as f:
            rapport_relu = json.loads(f.read())

        self.assertIn("horodatage", rapport_relu)
        self.assertIn("sites", rapport_relu)
        self.assertEqual(rapport_relu["sites"][0]["site"]["code"], "DKR")
        self.assertEqual(rapport_relu["sites"][0]["vent"], 13.4)
        self.assertEqual(rapport_relu["sites"][0]["alertes"], [])


if __name__ == "__main__":
    unittest.main()