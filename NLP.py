import spacy
nlp = spacy.load("es_core_news_sm")

# Nombre del archivo que contiene el texto completo
archivo_texto = "parrafos_ingredientes.txt"

with open(archivo_texto, "r", encoding="utf-8") as file:
    texto_completo = file.read()

doc = nlp(texto_completo)

#############################
from spacy.matcher import Matcher
# Definimos un patron para "Ingred Ientes" ya que así ha leido OCR los encabezados de Ingredientes
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

#############################

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


#############################
from spacy.matcher import Matcher, PhraseMatcher
import numpy as np
from spacy.tokens import Span, Doc
from spacy.language import Language
from collections import defaultdict, Counter

nlp = spacy.load("es_core_news_sm")

matcher = PhraseMatcher(nlp.vocab)
patrones_ingredientes = list(nlp.pipe(ingredientes_espanoles))
matcher.add("INGREDIENTES", None, *patrones_ingredientes)

# Define un componente personalizado para detectar ingredientes
@Language.component("detector_ingredientes")
def detectar_ingredientes(doc):
    matches = matcher(doc)
    spans = [Span(doc, start, end, label=match_id) for match_id, start, end in matches]
    doc.ents = spans
    return doc

# Añade el componente personalizado al pipeline de spaCy
nlp.add_pipe("detector_ingredientes")


#############################
import re

def separar_palabras(texto):
    # Patrón de búsqueda: una palabra seguida por una letra mayúscula y luego otra palabra
    patron = r'([a-zA-ZáéíóúÁÉÍÓÚñÑ]+)([A-Z0-9])([a-zA-ZáéíóúÁÉÍÓÚñÑ]*)'

    # Función de sustitución para insertar un espacio entre las palabras mal concatenadas
    def corregir_coincidencia(match):
        return f'{match.group(1)} {match.group(2).lower()}{match.group(3)}'

    # Aplicar la función de sustitución al texto utilizando el patrón
    texto_corregido = re.sub(patron, corregir_coincidencia, texto)

    return texto_corregido

def convertir_a_minusculas(texto):
    texto_minusculas = texto.lower()
    return texto_minusculas


# Diccionario para almacenar las relaciones entre los personajes
relaciones = defaultdict(Counter)


def procesar_relaciones(parrafos):
    # Iterate over each parrafo
    for index,parrafo in enumerate(parrafos):
        # Process the individual parrafo
        texto_tratado_1= separar_palabras(parrafo)
        texto_tratado_2= convertir_a_minusculas(texto_tratado_1)
        texto_tratado="".join(texto_tratado_2)

        parrafo = nlp(texto_tratado)

        # Lista para almacenar los ingredientes mencionados en la receta actual, comprobando que no aparezcan repetidos
        ingredientes_oracion=[]
        for entidad in parrafo.ents:
          if entidad.label_=="INGREDIENTES" and entidad.text not in ingredientes_oracion:
                ingredientes_oracion.append(entidad.text)

        # print(ingredientes_oracion)

        # Actualizar las relaciones basadas en la co-ocurrencia de personajes en la misma oración
        for ingrediente1 in ingredientes_oracion:
            for ingrediente2 in ingredientes_oracion:
                if ingrediente1 != ingrediente2:
                    relaciones[ingrediente1][ingrediente2] += 1

procesar_relaciones(parrafos)
