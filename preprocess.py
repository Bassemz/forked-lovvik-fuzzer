import fitz  # PyMuPDF
import re

def extract_ATT_sections_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    section_pattern = re.compile(r'\d+(\.\d+)+\.\s+ATT_\w+')  # e.g., 1, 1.1, 2.3.4

    replacements = {
        "_REQ": "_REQUEST",
        "_RSP": "_RESPONSE",
        "_CMD": "_COMMAND",
        "_IND": "_INDICATION",
        "_NTF": "_NOTIFICATION"
    }

    sections = []

    for page in doc:
        text = page.get_text("text")
        # print(text)
        for line in text.split('\n'):
            line = line.strip()
            # print(line)
            match = section_pattern.match(line)
            if match:
                text = match.string.split(" ")[1]
                for key, value in replacements.items():
                    text = text.replace(key, value)
                sections.append(text)

    return sections

# This function extracts all the elements of the list provided into a text file
def extract_to_text_file(elements, output="results/output.txt"):
    with open(output, 'w') as f:
        for element in elements:
            f.write(element + '\n')



if __name__ == "__main__":
    pdf_file = "docs/BLE-Attribute-Protocol-(ATT).pdf"
    sections = extract_ATT_sections_from_pdf(pdf_file)
    extract_to_text_file(sections)
