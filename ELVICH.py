import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


def choisir_couleur_type(type_noeud):
    """Retourne une couleur et une forme basées sur le type de nœud"""
    couleurs_types = {
        'hopital': {'color': '#4A90E2', 'shape': 'o'},
        'pharmacie': {'color': '#7ED321', 'shape': 's'},
        'docteur': {'color': '#F5A623', 'shape': '^'},
        'infirmiere': {'color': '#9013FE', 'shape': 'D'},
        'patient': {'color': '#D0021B', 'shape': 'v'},
        'ambulance': {'color': '#FF6B35', 'shape': 'p'},
        'pays': {'color': '#4A4A4A', 'shape': 'h'},
        'ville': {'color': '#8B572A', 'shape': 'H'},
        'quartier': {'color': '#417505', 'shape': '8'},
        'continent': {'color': '#2E3440', 'shape': '*'},
        'default': {'color': '#666666', 'shape': 'o'}
    }
    return couleurs_types.get(type_noeud.lower(), couleurs_types['default'])


def saisir_nombre_par_type():
    """Demande le nombre d'éléments pour chaque type"""
    print("=== CONFIGURATION DU SYSTÈME MÉDICAL ET GÉOGRAPHIQUE ===")
    print("Veuillez entrer le nombre d'éléments pour chaque type :")
    print("(Appuyez sur Entrée pour 0 si vous ne voulez pas d'éléments de ce type)\n")

    types_medicaux = {
        'hopital': 'Nombre d\'hôpitaux',
        'infirmiere': 'Nombre d\'infirmières',
        'patient': 'Nombre de patients',
        'ambulance': 'Nombre d\'ambulances',
        'docteur': 'Nombre de docteurs',
        'pharmacie': 'Nombre de pharmacies'
    }
    types_geographiques = {
        'continent': 'Nombre de continents',
        'pays': 'Nombre de pays',
        'ville': 'Nombre de villes',
        'quartier': 'Nombre de quartiers'
    }
    config = {}

    # Saisie des éléments médicaux
    print("--- ÉLÉMENTS MÉDICAUX ---")
    for type_noeud, description in types_medicaux.items():
        while True:
            try:
                input_value = input(f"{description} : ").strip()
                if input_value == "":
                    config[type_noeud] = 0
                    break
                else:
                    nombre = int(input_value)
                    if nombre >= 0:
                        config[type_noeud] = nombre
                        break
                    else:
                        print("Le nombre doit être positif ou nul.")
            except ValueError:
                print("Veuillez entrer un nombre entier valide ou appuyer sur Entrée pour 0.")

                # Saisie des éléments géographiques
    print("\n--- ÉLÉMENTS GÉOGRAPHIQUES ---")
    for type_noeud, description in types_geographiques.items():
        while True:
            try:
                input_value = input(f"{description} : ").strip()
                if input_value == "":
                    config[type_noeud] = 0
                    break
                else:
                    nombre = int(input_value)
                    if nombre >= 0:
                        config[type_noeud] = nombre
                        break
                    else:
                        print("Le nombre doit être positif ou nul.")
            except ValueError:
                print("Veuillez entrer un nombre entier valide ou appuyer sur Entrée pour 0.")

    return config


def saisir_noms_par_type(config):
    """Saisit les noms pour chaque type selon la configuration"""
    print("\n=== SAISIE DES NOMS ===")
    print("(Appuyez sur Entrée pour passer si vous ne voulez pas entrer de nom)\n")

    noeuds = {}

    # Ordre logique de saisie : du plus large au plus spécifique
    ordre_types = ['continent', 'pays', 'ville', 'quartier', 'hopital', 'docteur', 'infirmiere', 'patient', 'ambulance',
                   'pharmacie']

    for type_noeud in ordre_types:
        if type_noeud in config and config[type_noeud] > 0:
            print(f"\n--- {type_noeud.upper()}S ---")

            for i in range(1, config[type_noeud] + 1):
                # Saisie du nom
                nom_noeud = input(f"Entrez le nom du/de la {type_noeud} {i} (ou Entrée pour continuer) : ").strip()
                # Si l'utilisateur appuie sur Entrée, on génère un nom par défaut
                if not nom_noeud:
                    nom_noeud = f"{type_noeud.capitalize()}_{i}"
                    # Vérifier si le nom existe déjà
                while nom_noeud in noeuds:
                    print(f"Le nom '{nom_noeud}' existe déjà.")
                    nom_noeud = input(
                        f"Entrez un autre nom pour le/la {type_noeud} {i} (ou Entrée pour nom automatique) : ").strip()
                    if not nom_noeud:
                        nom_noeud = f"{type_noeud.capitalize()}_{i}_{len(noeuds)}"

                        # Saisie de la position (optionnel)
                try:
                    pos_input = input(
                        f"Position (x,y) pour '{nom_noeud}' (Entrée pour position automatique) : ").strip()
                    if pos_input:
                        x, y = map(float, pos_input.split(','))
                        position = (x, y)
                    else:
                        # Position aléatoire mais organisée par type
                        base_x = {
                            'continent': -6, 'pays': -4, 'ville': -2, 'quartier': 0,
                            'hopital': 2, 'docteur': 3, 'infirmiere': 4, 'patient': 6,
                            'ambulance': 8, 'pharmacie': 5
                        }
                        x_base = base_x.get(type_noeud, 0)
                        position = (x_base + np.random.uniform(-1, 1), np.random.uniform(-2, 2))
                except:
                    base_x = {
                        'continent': -6, 'pays': -4, 'ville': -2, 'quartier': 0,
                        'hopital': 2, 'docteur': 3, 'infirmiere': 4, 'patient': 6,
                        'ambulance': 8, 'pharmacie': 5
                    }
                    x_base = base_x.get(type_noeud, 0)
                    position = (x_base + np.random.uniform(-1, 1), np.random.uniform(-2, 2))

                noeuds[nom_noeud] = {
                    'type': type_noeud,
                    'pos': position
                }

    return noeuds


def saisir_relations_automatiques(noeuds):
    """Propose des relations automatiques ou permet la saisie manuelle"""
    print("\n=== CONFIGURATION DES RELATIONS ===")

    choix = input("Voulez-vous des relations automatiques ? (o/n) : ").strip().lower()

    if choix == 'o':
        return generer_relations_automatiques(noeuds)
    else:
        return saisir_relations_manuelles(noeuds)


def generer_relations_automatiques(noeuds):
    """Génère des relations logiques automatiques"""
    relations = []

    # Séparer les nœuds par type
    types_noeuds = {}
    for nom, data in noeuds.items():
        type_noeud = data['type']
        if type_noeud not in types_noeuds:
            types_noeuds[type_noeud] = []
        types_noeuds[type_noeud].append(nom)

    # Relations logiques automatiques
    relations_count = 1

    # Relations géographiques hiérarchiques
    # Pays appartiennent aux continents
    if 'pays' in types_noeuds and 'continent' in types_noeuds:
        for pays in types_noeuds['pays']:
            continent = np.random.choice(types_noeuds['continent'])
            relations.append((pays, continent, f"Appartient_à_{relations_count}"))
            relations_count += 1

            # Villes appartiennent aux pays
    if 'ville' in types_noeuds and 'pays' in types_noeuds:
        for ville in types_noeuds['ville']:
            pays = np.random.choice(types_noeuds['pays'])
            relations.append((ville, pays, f"Située_dans_{relations_count}"))
            relations_count += 1

            # Quartiers appartiennent aux villes
    if 'quartier' in types_noeuds and 'ville' in types_noeuds:
        for quartier in types_noeuds['quartier']:
            ville = np.random.choice(types_noeuds['ville'])
            relations.append((quartier, ville, f"Partie_de_{relations_count}"))
            relations_count += 1

            # Hôpitaux situés dans les quartiers ou villes
    if 'hopital' in types_noeuds:
        lieux = []
        if 'quartier' in types_noeuds:
            lieux.extend(types_noeuds['quartier'])
        elif 'ville' in types_noeuds:
            lieux.extend(types_noeuds['ville'])

        if lieux:
            for hopital in types_noeuds['hopital']:
                lieu = np.random.choice(lieux)
                relations.append((hopital, lieu, f"Situé_dans_{relations_count}"))
                relations_count += 1

                # Relations médicales
    # Connecter les infirmières aux hôpitaux
    if 'infirmiere' in types_noeuds and 'hopital' in types_noeuds:
        for infirmiere in types_noeuds['infirmiere']:
            hopital = np.random.choice(types_noeuds['hopital'])
            relations.append((infirmiere, hopital, f"Travaille_à_{relations_count}"))
            relations_count += 1

            # Connecter les docteurs aux hôpitaux
    if 'docteur' in types_noeuds and 'hopital' in types_noeuds:
        for docteur in types_noeuds['docteur']:
            hopital = np.random.choice(types_noeuds['hopital'])
            relations.append((docteur, hopital, f"Travaille_à_{relations_count}"))
            relations_count += 1

            # Connecter les patients aux docteurs et/ou infirmières
    if 'patient' in types_noeuds:
        soignants = []
        if 'docteur' in types_noeuds:
            soignants.extend(types_noeuds['docteur'])
        if 'infirmiere' in types_noeuds:
            soignants.extend(types_noeuds['infirmiere'])

        for patient in types_noeuds['patient']:
            if soignants:
                soignant = np.random.choice(soignants)
                relations.append((patient, soignant, f"Soigné_par_{relations_count}"))
                relations_count += 1

                # Connecter les ambulances aux hôpitaux
    if 'ambulance' in types_noeuds and 'hopital' in types_noeuds:
        for ambulance in types_noeuds['ambulance']:
            hopital = np.random.choice(types_noeuds['hopital'])
            relations.append((ambulance, hopital, f"Dessert_{relations_count}"))
            relations_count += 1

            # Connecter les pharmacies aux hôpitaux ou quartiers
    if 'pharmacie' in types_noeuds:
        lieux = []
        if 'hopital' in types_noeuds:
            lieux.extend(types_noeuds['hopital'])
        if 'quartier' in types_noeuds:
            lieux.extend(types_noeuds['quartier'])

        if lieux:
            for pharmacie in types_noeuds['pharmacie']:
                lieu = np.random.choice(lieux)
                relations.append((pharmacie, lieu, f"Proche_de_{relations_count}"))
                relations_count += 1

    print(f"\n{len(relations)} relations automatiques générées.")
    return relations