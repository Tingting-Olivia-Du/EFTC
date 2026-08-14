from pdfminer.high_level import extract_text

def pdf_to_text(input_pdf_path, output_txt_path):
    text = extract_text(input_pdf_path)
    with open(output_txt_path, 'w', encoding='utf-8') as output_file:
        output_file.write(text)
    print(f"Text extracted to {output_txt_path}")


input = 'F:/previous-FAWL/FAC_Project/texts/textbooks_pdf/01_corporate_finance/pdf/1_1_Stephen.pdf'
output = 'F:/research_file/FAWL_Python/textbooks_raw/1_1_pdfminer.txt'

# Usage
pdf_to_text(input, output)
