import sys
import unittest
sys.path.insert(0, '.')
from teranganet.audit import calculer_alertes


class TestCalculerAlertes(unittest.TestCase):
    def test_vent_au_dessus_du_seuil_avec_equipement_exterieur(self):
        alertes = calculer_alertes(
            vent=40, temperature=25,
            seuil_vent=35, seuil_temperature=35,
            a_equipement_exterieur=True
        )
        self.assertIn("VENT", alertes)

    def test_vent_en_dessous_du_seuil(self):
        alertes = calculer_alertes(
            vent=20, temperature=25,
            seuil_vent=35, seuil_temperature=35,
            a_equipement_exterieur=True
        )
        self.assertNotIn("VENT", alertes)

    def test_vent_au_dessus_du_seuil_sans_equipement_exterieur(self):
        alertes = calculer_alertes(
            vent=40, temperature=25,
            seuil_vent=35, seuil_temperature=35,
            a_equipement_exterieur=False
        )
        self.assertNotIn("VENT", alertes)

    def test_temperature_exactement_au_seuil(self):
        alertes = calculer_alertes(
            vent=10, temperature=35,
            seuil_vent=35, seuil_temperature=35,
            a_equipement_exterieur=True
        )
        self.assertIn("TEMPERATURE", alertes)

    def test_aucune_alerte_si_tout_est_bas(self):
        alertes = calculer_alertes(
            vent=10, temperature=20,
            seuil_vent=35, seuil_temperature=35,
            a_equipement_exterieur=True
        )
        self.assertEqual(alertes, [])


if __name__ == "__main__":
    unittest.main()