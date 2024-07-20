import spacy
nlp = spacy.load("es_core_news_sm")

archivo_texto = "parrafos_ingredientes.txt"

with open(archivo_texto, "r", encoding="utf-8") as file:
    texto_completo = file.read()
doc = nlp(texto_completo)

from spacy.matcher import Matcher
# [ES] Definimos un patron para "Ingred Ientes" ya que así ha leido OCR los encabezados de Ingredientes
# [EN] As OCR has read the headers as "Ingred Ientes" we define a pattern for it
matcher = Matcher(nlp.vocab)
patron = [{"TEXT":"Ingred"},{"TEXT":"Ientes"}]
matcher.add("recipe", [patron])

parrafos = []
start_index = 2
matches = matcher(doc)
for match_id, start, end in matches:
    parrafos.append(doc[start_index-2:end-2].text)
    start_index = end

parrafos.append(doc[start_index:].text)

# [ES] Todos los ingreedientes en español que se podrían encontrar en una receta
# [EN] All the ingredients in Spanish that could be found in a recipe
ingredientes_espanoles = [
    "ajo",
    "cebolla",
    "pimiento",
    "tomate",
    "patata",
    "berenjena",
    "calabacín",
    "pepino",
    "zanahoria",
    "espinacas",
    "alcachofa",
    "judías verdes",
    "guisantes",
    "setas",
    "champiñones",
    "garbanzos",
    "cebollino",
    "puerro",
    "maíz",
    "aceitunas",
    "anchoas",
    "atún en conserva",
    "bacalao",
    "gambas",
    "langostinos",
    "sepia",
    "pulpo",
    "vieiras",
    "mejillones",
    "almejas",
    "pollo",
    "conejo",
    "cerdo",
    "leche",
    "chorizo",
    "queso manchego",
    "queso cabra",
    "queso azul",
    "yogur",
    "nata",
    "mantequilla",
    "vinagre",
    "vino blanco",
    "vino tinto",
    "pan",
    "harina",
    "arroz",
    "pasta",
    "azúcar",
    "miel",
    "chocolate",
    "almendras",
    "nueces",
    "avellanas",
    "pimienta",
    "pimentón",
    "comino",
    "nuez moscada",
    "clavo",
    "canela",
    "azafrán",
    "tomillo",
    "romero",
    "orégano",
    "laurel",
    "perejil",
    "albahaca",
    "ajo en polvo",
    "cebolla en polvo",
    "sal",
    "aceitunas rellenas",
    "vino de Jerez",
    "limón",
    "naranja",
    "lima",
    "melon",
    "sandía",
    "agua",
    "ciruelas pasas",
    "higos secos",
    "orejones",
    "piñones",
    "aceite",
    "aguacate",
    "salmón",
    "bacalao",
    "langosta",
    "vino blanco",
    "huevo",
    "esparragos",
    "piña",
    "ketchup",
    "mayonesa",
    "marisco",
    "jamón",
    "galletas",
    "hojaldre"]


from spacy.matcher import Matcher, PhraseMatcher
import numpy as np
from spacy.tokens import Span, Doc
from spacy.language import Language
from collections import defaultdict, Counter

nlp = spacy.load("es_core_news_sm")
matcher = PhraseMatcher(nlp.vocab)
patrones_ingredientes = list(nlp.pipe(ingredientes_espanoles))
matcher.add("INGREDIENTES", None, *patrones_ingredientes)

# [ES] Define un componente personalizado para detectar ingredientes
# [EN] Define a custom component to detect ingredients
@Language.component("detector_ingredientes")
def detectar_ingredientes(doc):
    matches = matcher(doc)
    spans = [Span(doc, start, end, label=match_id) for match_id, start, end in matches]
    doc.ents = spans
    return doc

nlp.add_pipe("detector_ingredientes")


import re
# [ES] Función para separar palabras mal concatenadas, ya que OCR ha interpretado mal algunos espacios
# [EN] Function to separate badly concatenated words, as OCR has misinterpreted some spaces
def separar_palabras(texto):
    # [ES] Patrón de búsqueda: una palabra seguida por una letra mayúscula y luego otra palabra
    # [EN] Search pattern: a word followed by an uppercase letter and then another word
    patron = r'([a-zA-ZáéíóúÁÉÍÓÚñÑ]+)([A-Z0-9])([a-zA-ZáéíóúÁÉÍÓÚñÑ]*)'

    # [ES] Función de sustitución para insertar un espacio entre las palabras mal concatenadas
    # [EN] Substitution function to insert a space between the badly concatenated words
    def corregir_coincidencia(match):
        return f'{match.group(1)} {match.group(2).lower()}{match.group(3)}'

    texto_corregido = re.sub(patron, corregir_coincidencia, texto)
    return texto_corregido

# [ES] Función para convertir un texto a minúsculas
# [EN] Function to convert a text to lowercase
def convertir_a_minusculas(texto):
    texto_minusculas = texto.lower()
    return texto_minusculas


# [ES] Diccionario para almacenar las relaciones entre los personajes
# [EN] Dictionary to store the relationships between the characters
relaciones = defaultdict(Counter)

# [ES] Función para procesar las relaciones entre los ingredientes en un mismo parrafo
# [EN] Function to process the relationships between the ingredients in the same paragraph
def procesar_relaciones(parrafos):
    for index,parrafo in enumerate(parrafos):
        
        texto_tratado_1= separar_palabras(parrafo)
        texto_tratado_2= convertir_a_minusculas(texto_tratado_1)
        texto_tratado="".join(texto_tratado_2)
        parrafo = nlp(texto_tratado)

        # [ES] Lista para almacenar los ingredientes mencionados en la receta actual, comprobando que no aparezcan repetidos
        # [EN] List to store the ingredients mentioned in the current recipe, checking that they do not appear repeated
        ingredientes_oracion=[]
        for entidad in parrafo.ents:
          if entidad.label_=="INGREDIENTES" and entidad.text not in ingredientes_oracion:
                ingredientes_oracion.append(entidad.text)

        # [ES] Actualizar las relaciones basadas en la co-ocurrencia de personajes en la misma oración
        # [EN] Update the relationships based on the co-occurrence of characters in the same
        for ingrediente1 in ingredientes_oracion:
            for ingrediente2 in ingredientes_oracion:
                if ingrediente1 != ingrediente2:
                    relaciones[ingrediente1][ingrediente2] += 1

procesar_relaciones(parrafos)
