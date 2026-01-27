from extractor import extract_text, clean_extracted_terms
import os

EXTRACT_TERMS = True
CLEAN_TERMS = False

#PDF = "AHA_clinical_guidelines\Heart Failure Clinical Guidelines.pdf"
CLINICAL_GUIDELINES_FOLDER = "AHA_clinical_guidelines"
EXTRACTED_TERMS_FOLDER = "extracted_terms_1.txt"
COMBINED_TERMS_FILE = "combined_extracted_terms.txt"
FINAL_TERMS_FILE = "final_terms.txt"

FINISHED_FILES = ["Acute Myocarditis Clinical Guidelines.pdf",
                  "Aortic Disease Clinical Guidelines.pdf",
                  "Chronic Coronary Disease Clinical Guidelines.pdf",
                  "Heart Failure Clinical Guidelines.pdf",
                  "Peripheral Artery Disease Clinical Guidelines.pdf",
                  "Primary Prevention of Cardiovascular Disease.pdf"]

if __name__ == "__main__":

   
    if EXTRACT_TERMS:
        for file in os.listdir(CLINICAL_GUIDELINES_FOLDER):
            if file.endswith(".pdf") and file not in FINISHED_FILES:
                PDF = os.path.join(CLINICAL_GUIDELINES_FOLDER, file)
                print(f"Processing file: {PDF}")
                extract_text(PDF)

    if CLEAN_TERMS:
        with open(COMBINED_TERMS_FILE, 'w', encoding='utf-8') as combined_file:
            for file in os.listdir(EXTRACTED_TERMS_FOLDER):
                with open(os.path.join(EXTRACTED_TERMS_FOLDER, file), 'r', encoding='utf-8') as f:
                    content = f.read()
                    combined_file.write(content)
                    combined_file.write("\n\n")

        with open(COMBINED_TERMS_FILE, "r", encoding="utf-8") as f:
            terms = f.readlines()

        cleaned_terms = clean_extracted_terms(terms)

        with open(FINAL_TERMS_FILE, "w", encoding="utf-8") as f:
            for term in cleaned_terms:
                f.write(f"{term}\n")