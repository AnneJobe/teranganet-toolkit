
# TerangaNet Ops Toolkit

Outil CLI pour surveiller les conditions météo sur les sites TerangaNet (Dakar, Thiès, Saint-Louis) et lever des alertes en cas de vent fort ou de forte chaleur.

## Contexte

TerangaNet est un fournisseur d'accès Internet sénégalais exploitant trois POP (points de présence) à Dakar, Thiès et Saint-Louis. Les antennes extérieures sont sensibles au vent fort et les locaux techniques à la chaleur. Ce toolkit croise l'inventaire des équipements avec les conditions météo actuelles (API Open-Meteo) pour générer des audits et des alertes automatiques.

## Installation

1. Cloner le dépôt :
   ```bash
   git clone https://github.com/AnneJobe/teranganet-toolkit.git
   cd teranganet-toolkit
   ```

2. (Recommandé) Créer un environnement virtuel :
   ```bash
   python -m venv venv
   venv\Scripts\activate      # Windows
   source venv/bin/activate   # macOS/Linux
   ```

3. Installer les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Lister l'inventaire des équipements
```bash
python toolkit.py inventaire
```

### Détailler un équipement
```bash
python toolkit.py show ANT1-DKR
```

### Consulter la météo actuelle d'un site
```bash
python toolkit.py meteo DKR
```

### Lancer un audit complet (inventaire + météo + alertes)
```bash
python toolkit.py audit
```

### Générer un rapport JSON horodaté
```bash
python toolkit.py rapport
```
Le rapport est écrit dans `rapports/`.

### Consulter l'historique des rapports

```bash
python toolkit.py historique

## Configuration

Les seuils d'alerte (vent, température) sont définis dans `config.yaml` et peuvent être ajustés sans modifier le code.

## Tests

```bash
python -m unittest discover tests -v
```

## Structure du projet

```
teranganet-toolkit/
├── toolkit.py              # point d'entrée CLI
├── config.yaml             # seuils d'alerte
├── data/
│   └── equipements.yaml    # inventaire des sites et équipements
├── teranganet/
│   ├── inventaire.py       # classes Site, Equipement + chargement YAML
│   ├── meteo.py            # client API Open-Meteo
│   ├── audit.py            # logique d'alerte
│   └── rapport.py          # export JSON
└── tests/
    ├── test_inventaire.py
    └── test_audit.py
```

## Auteurs

- Anne Jobe
- Evrard Léonadin Gnimadi

## Contexte académique

Projet réalisé dans le cadre du parcours DevNet Associate, MIT — sujet fourni par Mamadou Bokhoum.