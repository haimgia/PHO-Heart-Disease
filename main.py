from extractor import extract_text
import os

#PDF = "AHA_clinical_guidelines\Heart Failure Clinical Guidelines.pdf"
FOLDER = "AHA_clinical_guidelines"

FINISHED_FILES = ["Acute Myocarditis Clinical Guidelines.pdf",
                  "Aortic Disease Clinical Guidelines.pdf",
                  "Chronic Coronary Disease Clinical Guidelines.pdf",
                  "Heart Failure Clinical Guidelines.pdf",
                  "Peripheral Artery Disease Clinical Guidelines.pdf",
                  "Primary Prevention of Cardiovascular Disease.pdf"]

if __name__ == "__main__":

    # for file in tqdm(os.listdir(FOLDER)):
    #     print(file)

    # exit()

    for file in os.listdir(FOLDER):
        if file.endswith(".pdf") and file not in FINISHED_FILES:
            PDF = os.path.join(FOLDER, file)
            print(f"Processing file: {PDF}")
            extract_text(PDF)