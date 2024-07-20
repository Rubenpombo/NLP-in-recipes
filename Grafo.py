# Libreria grafos
import networkx as nx
import matplotlib.pyplot as plt
from NLP import relaciones

# Crear un grafo vacío
G = nx.Graph()
# Añadir los nodos y las aristas al grafo
for ingrediente1, counts in relaciones.items():
    for ingrediente2, count in counts.items():
        if ingrediente1 != ingrediente2:
            G.add_edge(ingrediente1, ingrediente2, weight=count)

# Para posicionar los nodos usamos el algoritmo de Layout, que calcula la disposición de los nodos de manera que los nodos conectados con mayor peso estén más cerca entre sí
pos = nx.spring_layout(G, seed=3)
nx.draw(G,pos,with_labels=True,node_color='khaki', node_size=1000, font_size=9, font_color='black')


# Guardar la figura en un archivo
import os
output_folder = "outputs"
os.makedirs(output_folder, exist_ok=True)  

output_path = os.path.join(output_folder, "grafo.png")
plt.savefig(output_path)
plt.close() 


# Degree centrality
degree_dict = nx.degree_centrality(G)
print("\n Degree centrality:\n")
print(degree_dict)

# Betweenness centrality
betweenness=nx.betweenness_centrality(G)
print("\n Betweenness centrality:\n")
print(betweenness)

# Closeness centrality
closeness = nx.closeness_centrality(G)
print("\n Closeness centrality:\n")
print(closeness)

# Louvain community detection
from community import community_louvain
comunidades = community_louvain.best_partition(G)
colores_nodos = [comunidades[node] for node in G.nodes]

nx.draw(G, pos, with_labels=True, node_color=colores_nodos, node_size=1000, font_size=9, font_color='black')

# Guardar la figura de comunidades en la carpeta "outputs"
output_path_comunidades = os.path.join(output_folder, "grafo_comunidades.png")
plt.savefig(output_path_comunidades)
plt.close()  # Cerrar la figura para liberar memoria