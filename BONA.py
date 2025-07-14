def creer_graphe():
    """Fonction principale pour créer le graphe"""
    print("=== GÉNÉRATEUR DE GRAPHE MÉDICAL ET GÉOGRAPHIQUE ===")
    print("Bienvenue dans le générateur de réseau médical et géographique!\n")

    # Configuration des types et nombres
    config = saisir_nombre_par_type()

    # Vérifier qu'au moins un élément est configuré
    if sum(config.values()) == 0:
        print("Aucun élément configuré. Fin du programme.")
        return None, None

        # Saisie des noms
    noeuds = saisir_noms_par_type(config)

    # Affichage du résumé
    print(f"\n=== RÉSUMÉ ===")
    print("--- ÉLÉMENTS GÉOGRAPHIQUES ---")
    for type_geo in ['continent', 'pays', 'ville', 'quartier']:
        if type_geo in config and config[type_geo] > 0:
            print(f"{type_geo.capitalize()}s : {config[type_geo]}")

    print("\n--- ÉLÉMENTS MÉDICAUX ---")
    for type_med in ['hopital', 'docteur', 'infirmiere', 'patient', 'ambulance', 'pharmacie']:
        if type_med in config and config[type_med] > 0:
            print(f"{type_med.capitalize()}s : {config[type_med]}")

    print(f"\nTotal des nœuds : {len(noeuds)}")

    # Saisie des relations
    relations = saisir_relations_automatiques(noeuds)

    # Création du graphe
    G = nx.Graph()

    # Ajout des nœuds
    for nom_noeud, data in noeuds.items():
        G.add_node(nom_noeud, **data)

        # Ajout des relations
    for relation in relations:
        noeud1, noeud2, label = relation
        if noeud1 in noeuds and noeud2 in noeuds:
            G.add_edge(noeud1, noeud2, label=label)
        else:
            print(f"Attention: Relation ignorée ({noeud1} - {noeud2}) car un des nœuds n'existe pas.")

    return G, noeuds


def visualiser_graphe(G, noeuds):
    """Visualise le graphe créé"""
    plt.figure(figsize=(16, 12))
    ax = plt.gca()

    # Extraire les positions
    pos = nx.get_node_attributes(G, 'pos')

    # Dessiner les arêtes avec labels
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edges(G, pos, edge_color='gray', alpha=0.6, width=2)

    # Grouper les nœuds par type
    node_types = {}
    for nom_noeud, data in noeuds.items():
        type_noeud = data['type']
        if type_noeud not in node_types:
            node_types[type_noeud] = {'nodes': [], 'style': choisir_couleur_type(type_noeud)}
        node_types[type_noeud]['nodes'].append(nom_noeud)
