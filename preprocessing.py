# [ES] La libreria PyPDF2 permite leer archivos PDF, y extraer texto de ellos.
# [EN] The PyPDF2 library allows you to read PDF files, and extract text from them.
import PyPDF2
import re
from tqdm import tqdm

def extract_ingredients(pdf_path='./recetas.pdf', start_page=11, end_page=None, step=2):
    """
    Extract ingredients from recipe PDF with improved error handling and progress tracking.
    
    Args:
        pdf_path: Path to the PDF file
        start_page: First page to extract (default: 11)
        end_page: Last page to extract (default: None, goes to end of file)
        step: Page step (default: 2 for odd pages)
    
    Returns:
        List of extracted text from each page
    """

    pdf_reader = PyPDF2.PdfReader(pdf_path)
    texto_ingredientes = []

    if end_page is None:
        end_page = len(pdf_reader.pages)-1
    
    print(f"Extracting ingredients from pages {start_page} to {end_page} with step {step}...")
    total_processed = 0

    # [ES] Se extrae el texto de las páginas impares, que contienen los ingredientes de las recetas.
    # [EN] Extract the text from the odd pages, which contain the ingredients of the recipes.
    for page_num in tqdm(range(start_page, end_page, step)):
        try:
            pag_receta = pdf_reader.pages[page_num]
            texto = pag_receta.extract_text()
            
            # Basic text cleaning during extraction
            texto = re.sub(r'\s+', ' ', texto).strip()
            texto_ingredientes.append(texto)
            total_processed += 1
        except Exception as e:
            print(f"Error processing page {page_num}: {e}")

    print(f"Successfully extracted text from {total_processed} pages")
    return texto_ingredientes


if __name__ == "__main__":
    texto_ingredientes = extract_ingredients()
    
    # [ES] Imprime una muestra de los ingredientes extraídos para verificar la calidad del texto.
    # [EN] Print a sample of the extracted ingredients to verify the quality of the text.
    for i in range(min(3, len(texto_ingredientes))):
        print(f"--- Ingredientes de la receta {i+1} (muestra) ---")
        print(texto_ingredientes[i][:150] + "...")
    
    # [ES] Une todos los textos extraídos en un solo string
    # [EN] Join all extracted texts into a single string
    texto_completo = "\n".join(texto_ingredientes)
    
    try:
        with open("parrafos_ingredientes.txt", "w", encoding="utf-8") as file:
            file.write(texto_completo)
        print(f"Saved {len(texto_ingredientes)} recipes to parrafos_ingredientes.txt")
    except Exception as e:
        print(f"Error saving text file: {e}")
