import networkx as nx
import matplotlib.pyplot as plt
from nlp import relaciones

# [ES] Se crea el grafo inicial representando las relaciones entre los ingredientes
# [EN] The initial graph is created representing the relationships between the ingredients
G_initial = nx.Graph()
for ingrediente1, counts in relaciones.items():
    for ingrediente2, count in counts.items():
        if ingrediente1 != ingrediente2:
            G_initial.add_edge(ingrediente1, ingrediente2, weight=count)

# [ES] Algoritmo layout para posicionar los nodos, que calcula la posición de los nodos de manera que los nodos conectados con mayor peso estén más cerca entre sí
# [EN] Layout algorithm to position the nodes, which calculates the arrangement of the nodes so that the nodes connected with greater weight are closer to each other
pos_initial = nx.spring_layout(G_initial, seed=3, k=0.6)
nx.draw(G_initial, pos_initial, with_labels=True, node_color='khaki', node_size=1000, font_size=9, font_color='black')

# [ES] Los resultados se guardan en la carpeta outputs
# [EN] The results are saved in the outputs folder
import os
output_folder = "outputs"
os.makedirs(output_folder, exist_ok=True)  
output_path = os.path.join(output_folder, "graph.png")
plt.savefig(output_path)
plt.close() 



# [ES] Analisis de las conexiones más importantes del grafo
# [EN] Analysis of the most important connections in the graph
G_best = nx.Graph()
for ingrediente1, counts in relaciones.items():
    for ingrediente2, count in counts.items():
        if ingrediente1 != ingrediente2 and count > 2:
            G_best.add_edge(ingrediente1, ingrediente2, weight=count)

pos_best = nx.spring_layout(G_best, seed=3, k=0.6)
nx.draw(G_best, pos_best, with_labels=True, node_color='khaki', node_size=1000, font_size=9, font_color='black')
nx.draw_networkx_edge_labels(G_best, pos_best, edge_labels=nx.get_edge_attributes(G_best, 'weight'))

output_path = os.path.join(output_folder, "important_connections.png")
plt.savefig(output_path)
plt.close() 



# [ES] Centralidad de grado
# [EN] Degree centrality
degree_dict = nx.degree_centrality(G_best)
print("\n Degree centrality:\n")
print(degree_dict)

# [ES] Centralidad de intermediación
# [EN] Betweenness centrality
betweenness=nx.betweenness_centrality(G_best)
print("\n Betweenness centrality:\n")
print(betweenness)

# [ES] Centralidad de cercanía
# [EN] Closeness centrality
closeness = nx.closeness_centrality(G_best)
print("\n Closeness centrality:\n")
print(closeness)



# [ES] Algoritmo de detección de comunidades Louvain en el grafo inicial
# [EN] Louvain community detection on the initial graph
from community import community_louvain
comunidades = community_louvain.best_partition(G_initial)
colores_nodos = [comunidades[node] for node in G_initial.nodes]
nx.draw(G_initial, pos_initial, with_labels=True, node_color=colores_nodos, node_size=1000, font_size=9, font_color='black')

output_path_comunidades = os.path.join(output_folder, "communities.png")
plt.savefig(output_path_comunidades)
plt.close() 
