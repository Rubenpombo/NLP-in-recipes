# NLP-in-recipes 📖 🥘
Through text mining, this project examined which ingredients were most frequently used together in Spanish cuisine recipes.
## Motivation
This project was completed for the course "Text Mining" at the University of Oviedo. My objective was to explore how analysis and conclusions can be drawn from large amounts of text, in this case, from a large book of recipes. 

## Files Description
### Preprocessing
Using `PyPDF2`, the code extracts ingredient data from recetas.pdf. After examining the book, it was found that recipe ingredients are listed on odd pages starting from page 11 up to page 95. The extracted ingredients are stored in parrafos_ingredientes.txt for additional analysis.

### NLP Analysis
The library `Spacy` parsed and segmented the file parrafos_ingredientes.txt into recipe sections. Each recipe's ingredient list is identified using a Matcher to delineate recipe boundaries. A predefined list of common Spanish ingredients is labeled as "INGREDIENTES" using a PhraseMatcher. A custom spaCy component integrates this matcher to detect ingredient entities throughout the text. Co-occurrence relationships between ingredients within each recipe are then analyzed and stored in a dictionary structure.

### Graph representation
Using the `networkx` library, the relationships between ingredients were represented as graphs. Various centrality measurements, such as closeness and betweenness, were applied to analyze these relationships. This analysis provided insights into the most central ingredients and their importance in Spanish cuisine recipes. Finally, the Louvain community detection algorithm classified the ingredients into communities based on their positions in the graph.
