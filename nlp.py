import spacy
import re
import json
import os
from spacy.matcher import Matcher
from spacy.matcher import Matcher, PhraseMatcher
from spacy.tokens import Span, Doc
from spacy.language import Language
from collections import defaultdict, Counter

# [ES] Cargamos el modelo de español preentrenado 'es_core_news_sm'
# [EN] Load the pre-trained Spanish language model 'es_core_news_sm'
nlp = spacy.load("es_core_news_sm")

# --------------------------------------
# 1. TEXT PROCESSING FUNCTIONS
# --------------------------------------
def separar_palabras(texto):
    """
    [ES] Separa palabras mal concatenadas en un texto. 
        Patrón de búsqueda: una palabra seguida por una letra mayúscula y luego otra palabra
    [EN] Separates badly concatenated words in a text
        Search pattern: a word followed by an uppercase letter and then another word
    """
    patron = r'([a-zA-ZáéíóúÁÉÍÓÚñÑ]+)([A-Z0-9])([a-zA-ZáéíóúÁÉÍÓÚñÑ]*)'
    
    def corregir_coincidencia(match):
        return f'{match.group(1)} {match.group(2).lower()}{match.group(3)}'
    
    texto_corregido = re.sub(patron, corregir_coincidencia, texto)
    return texto_corregido

def normalize_text(text):
    """Apply all text normalization steps in sequence"""
    text = separar_palabras(text)
    text = text.lower().strip()
    return text

def normalize_ingredient(ingredient_text):
    """Normalize ingredient name using synonyms if available"""
    normalized = ingredient_text.lower().strip()
    return INGREDIENT_SYNONYMS.get(normalized, normalized)


# --------------------------------------
# 2. INGREDIENT DETECTION SETUP
# --------------------------------------

# [ES] Todos los ingreedientes en español que se podrían encontrar en una receta
# [EN] All the ingredients in Spanish that could be found in a recipe
spanish_ingredients = [
    "ajo", "cebolla", "pimiento", "tomate", "patata", "berenjena", "calabacín", "pepino", "zanahoria", "espinacas",
    "alcachofa", "judías verdes", "guisantes", "setas", "champiñones", "garbanzos", "cebollino", "puerro", "maíz", "aguacate",
    "aceitunas", "aceitunas rellenas", "limón", "naranja", "lima", "melon", "sandía", "piña", "ciruelas pasas", "higos secos",
    "orejones", "piñones", "sal", "pimienta", "pimentón", "comino", "nuez moscada", "clavo", "canela", "azafrán",
    "tomillo", "romero", "orégano", "laurel", "perejil", "albahaca", "aceite", "vinagre", "agua", "harina",
    "arroz", "pasta", "pan", "azúcar", "miel", "chocolate", "almendras", "nueces", "avellanas", "galletas",
    "hojaldre", "ketchup", "mayonesa", "huevo", "leche", "nata", "yogur", "mantequilla", "queso manchego", "queso cabra",
    "queso azul", "pollo", "conejo", "cerdo", "chorizo", "jamón", "atún en conserva", "anchoas", "salmón", "bacalao",
    "gambas", "langostinos", "sepia", "pulpo", "vieiras", "mejillones", "almejas", "langosta", "marisco", "esparragos"
]

INGREDIENT_SYNONYMS = {
    "ajo en polvo": "ajo",
    "cebolla en polvo": "cebolla",
    "vino blanco": "vino",
    "vino tinto": "vino",
    "vino de jerez": "vino",
    "queso manchego": "queso",
    "queso cabra": "queso",
    "queso azul": "queso",
}


@Language.component("detector_ingredientes")
def detectar_ingredientes(doc):
    """[ES] Detecta ingredientes en el texto y los marca como entidades
       [EN] Detects ingredients in the text and marks them as entities"""
    matches = matcher(doc)
    spans = [Span(doc, start, end, label=match_id) for match_id, start, end in matches]
    doc.ents = spans
    return doc


def setup_nlp_pipeline():
    """Set up the NLP pipeline with ingredient detection"""
    global matcher
    
    # Create phrase matcher for ingredients
    matcher = PhraseMatcher(nlp.vocab)
    patrones_ingredientes = list(nlp.pipe(spanish_ingredients))
    matcher.add("INGREDIENTES", None, *patrones_ingredientes)
    
    # Configure pipeline
    if "detector_ingredientes" not in nlp.pipe_names:
        nlp.add_pipe("detector_ingredientes")
    
    return nlp


# --------------------------------------
# 3. LOADING AND PARSING TEXT
# --------------------------------------
def load_ingredients_text(file_path="parrafos_ingredientes.txt"):
    """Load the ingredients text file created by preprocessing.py"""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            texto_completo = file.read()
        
        # Process the full document
        doc = nlp(texto_completo)
        
        # Define matcher for recipe headers
        header_matcher = Matcher(nlp.vocab)
        patron = [{"TEXT":"Ingred"},{"TEXT":"Ientes"}]
        header_matcher.add("recipe", [patron])
        
        # Find all recipe headers
        matches = header_matcher(doc)
        
        # Extract recipe paragraphs
        parrafos = []
        start_index = 2  # Starting from beginning
        
        for match_id, start, end in matches:
            parrafos.append(doc[start_index-2:end-2].text)
            start_index = end
        
        # Don't forget the last paragraph
        parrafos.append(doc[start_index:].text)
        
        print(f"Loaded and parsed {len(parrafos)} recipe sections")
        return parrafos
    except Exception as e:
        print(f"Error loading ingredients text: {e}")
        return []


# --------------------------------------
# 4. ANALYZING INGREDIENT RELATIONSHIPS
# --------------------------------------
def build_ingredient_relationships(parrafos):
    """[ES] Construye un diccionario de relaciones entre ingredientes
       [EN] Builds a dictionary of relationships between ingredients"""
    # Dictionary to store relationships
    relaciones = defaultdict(Counter)
    
    # Setup NLP pipeline
    nlp = setup_nlp_pipeline()
    
    # Process each recipe paragraph
    for idx, parrafo in enumerate(parrafos):
        # Normalize text
        texto_tratado = normalize_text(parrafo)
        doc = nlp(texto_tratado)
        
        # Extract unique ingredients from this recipe
        ingredientes_receta = []
        for entidad in doc.ents:
            if entidad.label_ == "INGREDIENTES":
                # Apply normalization to handle synonyms
                normalized_ingredient = normalize_ingredient(entidad.text)
                if normalized_ingredient not in ingredientes_receta:
                    ingredientes_receta.append(normalized_ingredient)
        
        # Update co-occurrence relationships
        for ingrediente1 in ingredientes_receta:
            for ingrediente2 in ingredientes_receta:
                if ingrediente1 != ingrediente2:
                    relaciones[ingrediente1][ingrediente2] += 1
    
    print(f"Found relationships between {len(relaciones)} ingredients")
    return relaciones

# --------------------------------------
# 5. FILE I/O FUNCTIONS
# --------------------------------------
def save_relationships(relaciones, output_file="outputs/relaciones.json"):
    """Save relationships to JSON for later use"""
    import os
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Convert to serializable format
    serializable = {}
    for ing1, counts in relaciones.items():
        serializable[ing1] = dict(counts)
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(serializable, f, ensure_ascii=False, indent=2)
    
    print(f"Saved relationships to {output_file}")


def load_relationships(input_file="outputs/relaciones.json"):
    """Load relationships from JSON"""
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # Convert back to Counter
    result = defaultdict(Counter)
    for ing1, counts in data.items():
        result[ing1].update(counts)
    
    return result


if __name__ == "__main__":
    archivo_texto = "parrafos_ingredientes.txt"
    
    # Load the preprocessed text and parse it into recipe paragraphs
    parrafos = load_ingredients_text(archivo_texto)

    # Build and save ingredient relationships
    relaciones = build_ingredient_relationships(parrafos)
    save_relationships(relaciones)