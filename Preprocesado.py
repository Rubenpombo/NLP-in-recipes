import PyPDF2

pdf_reader = PyPDF2.PdfReader('./recetas.pdf')

texto_ingredientes = []

for page_num in range(11, len(pdf_reader.pages)-1, 2):
    pag_receta = pdf_reader.pages[page_num]
    texto= pag_receta.extract_text()

    # Guardamos las paginas
    texto_ingredientes.append(texto)


for i in range(len(texto_ingredientes)):
    print(f"--- Ingredientes de la receta {i}---")
    print(texto_ingredientes[i])

############################################

# Unir todo el texto de las páginas en una sola cadena
texto_ingredientes = "\n".join(texto_ingredientes)

# Guardar el texto completo en un archivo de texto
with open("parrafos_ingredientes.txt", "w", encoding="utf-8") as file:
    file.write(texto_ingredientes)


