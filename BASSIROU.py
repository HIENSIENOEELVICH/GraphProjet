 # Dessiner chaque type de nœud
    for type_noeud, type_data in node_types.items():
        if type_data['nodes']:
            nx.draw_networkx_nodes(G, pos,
                                   nodelist=type_data['nodes'],
                                   node_color=type_data['style']['color'],
                                   node_shape=type_data['style']['shape'],
                                   node_size=2500,
                                   alpha=0.8)

            # Ajouter les labels des nœuds
     nx.draw_networkx_labels(G, pos, font_size=9, font_weight='bold')

    # Ajouter les labels des arêtes
    if edge_labels:
        edge_labels_pos = {}
        for edge in G.edges():
            x1, y1 = pos[edge[0]]
            x2, y2 = pos[edge[1]]
            edge_labels_pos[edge] = ((x1 + x2) / 2, (y1 + y2) / 2)

        for edge, label in edge_labels.items():
            x, y = edge_labels_pos[edge]
            plt.text(x, y, label, fontsize=7, ha='center', va='center',
                     bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))

            # Créer la légende
    legend_elements = []
    for type_noeud, type_data in node_types.items():
        if type_data['nodes']:
            legend_elements.append(plt.Line2D([0], [0], marker=type_data['style']['shape'],
                                              color='w', markerfacecolor=type_data['style']['color'],
                                              markersize=12,
                                              label=f"{type_noeud.capitalize()} ({len(type_data['nodes'])})"))

    if legend_elements:
        plt.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1, 1))

        # Configuration du graphique
    plt.title('Réseau Médical et Géographique - Théorie des Graphes',
              fontsize=16, fontweight='bold', pad=20)
    plt.axis('off')
    plt.tight_layout()

    # Afficher le graphique
    plt.show()


def afficher_statistiques(G):
    """Affiche les statistiques du graphe"""
    print("\n=== STATISTIQUES DU RÉSEAU MÉDICAL ET GÉOGRAPHIQUE ===")
    print(f"Nombre total de nœuds: {G.number_of_nodes()}")
    print(f"Nombre total de relations: {G.number_of_edges()}")

    if G.number_of_nodes() > 1:
        print(f"Densité du réseau: {nx.density(G):.3f}")
        print(f"Le réseau est-il connexe? {nx.is_connected(G)}")

        # Afficher les degrés des nœuds
        print("\n=== CONNEXIONS PAR NŒUD ===")
        degrees = dict(G.degree())
        for node, degree in sorted(degrees.items(), key=lambda x: x[1], reverse=True):
            print(f"{node}: {degree} connexions")

            # Afficher les composantes connexes
        print("\n=== COMPOSANTES CONNEXES ===")
        components = list(nx.connected_components(G))
        print(f"Nombre de composantes connexes: {len(components)}")
        for i, component in enumerate(components, 1):
            print(f"Composante {i}: {list(component)}")

            # Calculer les métriques de centralité
        print("\n=== NŒUDS LES PLUS CENTRAUX ===")
        try:
            centrality = nx.betweenness_centrality(G)
            print("Centralité d'intermédiarité (top 5):")
            for node, cent in sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:5]:
                print(f"  {node}: {cent:.3f}")
        except:
            print("Impossible de calculer la centralité d'intermédiarité")
    else:
        print("Réseau trop petit pour les statistiques avancées.")


def main():
    """Fonction principale du programme"""
    try:
        # Créer le graphe
        resultat = creer_graphe()
        if resultat[0] is None:
            return

        G, noeuds = resultat

        # Visualiser le graphe
        print("\n=== GÉNÉRATION DU GRAPHIQUE ===")
        visualiser_graphe(G, noeuds)

        # Afficher les statistiques
        afficher_statistiques(G)

        print("\n=== TERMINÉ ===")
        print("Votre réseau médical et géographique a été généré avec succès!")
    except KeyboardInterrupt:
        print("\n\nProgramme interrompu par l'utilisateur.")
    except Exception as e:
        print(f"\nErreur lors de la génération du graphe: {e}")


# Lancer le programme
if __name__ == "__main__":
    main()