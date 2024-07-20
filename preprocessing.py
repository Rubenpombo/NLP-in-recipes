# [ES] La libreria PyPDF2 permite leer archivos PDF, y extraer texto de ellos.
# [EN] The PyPDF2 library allows you to read PDF files, and extract text from them.
import PyPDF2
pdf_reader = PyPDF2.PdfReader('./recetas.pdf')
texto_ingredientes = []

# [ES] Se extrae el texto de las páginas impares, que contienen los ingredientes de las recetas.
# [EN] Extract the text from the odd pages, which contain the ingredients of the recipes.
for page_num in range(11, len(pdf_reader.pages)-1, 2):
    pag_receta = pdf_reader.pages[page_num]
    texto= pag_receta.extract_text()

    texto_ingredientes.append(texto)


for i in range(len(texto_ingredientes)):
    print(f"--- Ingredientes de la receta {i}---")
    print(texto_ingredientes[i])


# [ES] Se une todo el texto de las páginas en una sola cadena
# [EN] All the text of the pages is joined into a single string
texto_ingredientes = "\n".join(texto_ingredientes)

# [ES] Se guarda el texto completo en un archivo de texto
# [EN] The complete text is saved in a text file
with open("parrafos_ingredientes.txt", "w", encoding="utf-8") as file:
    file.write(texto_ingredientes)


