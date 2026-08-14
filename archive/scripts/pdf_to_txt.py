import fitz  # PyMuPDF

def pdf_to_text(input_pdf_path, output_txt_path):
    # Open the PDF file
    pdf_document = fitz.open(input_pdf_path)
    with open(output_txt_path, 'w', encoding='utf-8') as output_file:
        # Extract text from each page
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            text = page.get_text()
            output_file.write(text)
    print(f"Text extracted to {output_txt_path}")

# Usage
input = 'F:/previous-FAWL/FAC_Project/texts/textbooks_pdf/01_corporate_finance/pdf/1_1_Stephen.pdf'
output = 'F:/research_file/FAWL_Python/textbooks_raw/1_1.txt'

pdf_to_text(input, output)
