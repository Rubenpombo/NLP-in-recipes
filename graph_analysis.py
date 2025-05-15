import networkx as nx
import matplotlib.pyplot as plt
import os
import json
from collections import defaultdict, Counter
import numpy as np
from community import community_louvain
from nlp import load_relationships, normalize_ingredient

# Import data from NLP module
try:
    from nlp import relaciones
except ImportError:
    # If relaciones is not available, try to load it
    relaciones = None

# --------------------------------------
# 1. GRAPH CREATION FUNCTIONS
# --------------------------------------

def create_ingredient_graph(relationships, min_weight=1):
    """
    Create a graph from ingredient relationships
    
    Args:
        relationships: Dictionary of ingredient relationships
        min_weight: Minimum weight to include an edge (default: 1)
        
    Returns:
        NetworkX graph object
    """
    G = nx.Graph()
    
    for ingrediente1, counts in relationships.items():
        for ingrediente2, count in counts.items():
            if ingrediente1 != ingrediente2 and count >= min_weight:
                G.add_edge(ingrediente1, ingrediente2, weight=count)
    
    print(f"Created graph with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")
    return G

# --------------------------------------
# 2. VISUALIZATION FUNCTIONS
# --------------------------------------

def visualize_graph(G, pos=None, show_weights=False, node_color='khaki', 
                   title="Ingredient Relationships", output_file=None):
    """
    Visualize a graph with customizable options
    
    Args:
        G: NetworkX graph to visualize
        pos: Node positions (if None, spring_layout will be used)
        show_weights: Whether to show edge weights
        node_color: Color for the nodes
        title: Title for the plot
        output_file: Path to save the visualization (if None, just displays)
    """
    plt.figure(figsize=(14, 12))
    
    # Calculate node positions if not provided
    if pos is None:
        pos = nx.spring_layout(G, seed=3, k=0.6)
    
    # Adjust node sizes based on connectivity
    node_sizes = []
    for node in G.nodes():
        # Size proportional to number of connections
        size = 800 + (G.degree(node) * 50)
        node_sizes.append(size)
    
    # Draw the graph
    nx.draw(G, pos, with_labels=True, 
            node_color=node_color, 
            node_size=node_sizes,
            font_size=9, font_weight='bold', font_color='black')
    
    # Add edge weights if requested
    if show_weights:
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
    
    plt.title(title, fontsize=16)
    
    # Save or show the plot
    if output_file:
        output_folder = os.path.dirname(output_file)
        if output_folder and not os.path.exists(output_folder):
            os.makedirs(output_folder, exist_ok=True)
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"Saved visualization to {output_file}")
    else:
        plt.show()
    
    return pos

# --------------------------------------
# 3. ANALYSIS FUNCTIONS
# --------------------------------------

def analyze_centrality(G):
    """
    Analyze various centrality metrics for a graph
    
    Args:
        G: NetworkX graph to analyze
        
    Returns:
        Dictionary containing the centrality measures
    """
    # Calculate centrality metrics
    degree_cent = nx.degree_centrality(G)
    betweenness_cent = nx.betweenness_centrality(G)
    closeness_cent = nx.closeness_centrality(G)
    
    # Sort ingredients by each centrality measure
    sorted_degree = sorted(degree_cent.items(), key=lambda x: x[1], reverse=True)
    sorted_betweenness = sorted(betweenness_cent.items(), key=lambda x: x[1], reverse=True)
    sorted_closeness = sorted(closeness_cent.items(), key=lambda x: x[1], reverse=True)
    
    # Print top ingredients for each measure
    print("\nTop ingredients by degree centrality:")
    for ingredient, value in sorted_degree[:10]:
        print(f"  {ingredient}: {value:.4f}")
    
    print("\nTop ingredients by betweenness centrality:")
    for ingredient, value in sorted_betweenness[:10]:
        print(f"  {ingredient}: {value:.4f}")
    
    print("\nTop ingredients by closeness centrality:")
    for ingredient, value in sorted_closeness[:10]:
        print(f"  {ingredient}: {value:.4f}")
    
    return {
        "degree": degree_cent,
        "betweenness": betweenness_cent,
        "closeness": closeness_cent
    }

def detect_communities(G, pos=None):
    """
    Detect and visualize communities in the graph
    
    Args:
        G: NetworkX graph
        pos: Node positions (optional)
        
    Returns:
        Dictionary of community memberships
    """
    
    # Detect communities
    communities = community_louvain.best_partition(G)
    
    # Count ingredients in each community
    community_counts = defaultdict(int)
    for node, community_id in communities.items():
        community_counts[community_id] += 1
    
    # Print community information
    print("\nDetected communities:")
    for community_id, count in sorted(community_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  Community {community_id}: {count} ingredients")
    
    # Visualize communities if possible
    if pos is not None:
        plt.figure(figsize=(14, 12))
        colors = [communities[node] for node in G.nodes()]
        
        # Draw graph with community colors
        nx.draw(G, pos, with_labels=True, 
                node_color=colors, cmap=plt.cm.tab20,
                node_size=1000, font_size=9, font_color='black')
        
        plt.title("Ingredient Communities", fontsize=16)
        
        # Save visualization
        output_folder = "outputs"
        os.makedirs(output_folder, exist_ok=True)
        output_path = os.path.join(output_folder, "communities.png")
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"Saved community visualization to {output_path}")
    
    return communities

# --------------------------------------
# 4. MAIN EXECUTION
# --------------------------------------

def main():
    """Main analysis workflow"""
    global relaciones
    
    # Ensure we have relationship data
    if relaciones is None:
        try:
            print("Loading ingredient relationships from file...")
            relaciones = load_relationships()
        except Exception as e:
            print(f"Error loading relationships: {e}")
            print("Please run nlp.py first to generate relationship data.")
            return
    
    # Create output directory
    output_folder = "outputs"
    os.makedirs(output_folder, exist_ok=True)
    
    # 1. Create and visualize the complete graph
    print("\n=== Creating complete ingredient graph ===")
    G_initial = create_ingredient_graph(relaciones)
    pos_initial = visualize_graph(
        G_initial, 
        title="Complete Ingredient Relationships",
        output_file=os.path.join(output_folder, "graph.png")
    )
    
    # 2. Create and visualize important connections
    print("\n=== Analyzing important connections ===")
    G_best = create_ingredient_graph(relaciones, min_weight=3)
    pos_best = visualize_graph(
        G_best,
        show_weights=True,
        title="Important Ingredient Relationships (weight ≥ 3)",
        output_file=os.path.join(output_folder, "important_connections.png")
    )
    
    # 3. Analyze centrality measures
    print("\n=== Analyzing centrality measures ===")
    centrality = analyze_centrality(G_best)
    
    # Save centrality data to file
    with open(os.path.join(output_folder, "centrality.json"), "w", encoding="utf-8") as f:
        # Convert to serializable format
        serializable = {}
        for measure, values in centrality.items():
            serializable[measure] = {ingredient: float(value) for ingredient, value in values.items()}
        json.dump(serializable, f, ensure_ascii=False, indent=2)
    
    # 4. Detect and visualize communities
    print("\n=== Detecting ingredient communities ===")
    communities = detect_communities(G_initial, pos_initial)
    
    # Save community data to file
    if communities:
        with open(os.path.join(output_folder, "communities.json"), "w", encoding="utf-8") as f:
            # Convert to serializable format
            json.dump(communities, f, ensure_ascii=False, indent=2)
    
    print("\nAll analyses complete. Results saved to the 'outputs' folder.")


if __name__ == "__main__":
    main()