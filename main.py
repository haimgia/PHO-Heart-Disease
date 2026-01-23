from extractor import extract_text
import os
from tqdm import tqdm

#PDF = "AHA_clinical_guidelines\Heart Failure Clinical Guidelines.pdf"
FOLDER = "AHA_clinical_guidelines"

if __name__ == "__main__":

    for file in tqdm(os.listdir(FOLDER)):
        if file.endswith(".pdf"):
            PDF = os.path.join(FOLDER, file)
            extract_text(PDF)