from urllib import response
import pymupdf
from openai import OpenAI
from tqdm import tqdm
from dotenv import load_dotenv
import os
import ollama


OUTPUT_DIR = "extracted_terms"

load_dotenv()

OPEN_ROUTER_API_KEY = os.getenv("OPEN_ROUTER_API_KEY")

GPT_OSS_ENDPOINT = os.getenv("GPT-OSS-ENDPOINT")

def extract_text(pdf_file):
    doc = pymupdf.open(pdf_file) # open a document

    # makes the output file path
    output_file = pdf_file.replace('.pdf', '_extracted_terms.txt')

    # create output directory if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open (os.path.join(OUTPUT_DIR, os.path.basename(output_file)), 'w', encoding='utf-8') as f:
        for i, page in tqdm(enumerate(doc)): # iterate the document pages
            text = page.get_text().encode("utf8") # get plain text (is in UTF-8)

            terms = extract_concepts(text.decode('utf8'))
            print(f"Extracted terms from page {i + 1}:\n {terms}\n")
            f.write(f"Page {i + 1} Extracted Terms:\n{terms}\n\n")


def extract_concepts(text):

    # calls openrouter API
    client = OpenAI(
        base_url=GPT_OSS_ENDPOINT
    )

    # API call to extract concepts
    response = client.chat.completions.create(
    model="gpt-oss-20b",
    messages=[
            {"role": "system", "content": "You are an expert at extracting terms related to heart disease from clinical guidelines."},
            {"role": "user", "content": f"Extract key terms related to heart disease from the following text:\n\n{text}\n\nFormat the output as a list of terms."}
            ]
    )

    # Extract the assistant message with reasoning_details
    response = response.choices[0].message

    terms = response.content
    # Implement concept extraction logic here
    return terms

def extract_concepts_ollama(text):
    print("Extracting concepts using Ollama...")
    messages = [
        {
            "role": "system",
            "content": "You are an expert at extracting terms related to heart disease from clinical guidelines."
        },
        {
            "role": "user",
            "content": (
                "Extract key terms related to heart disease from the following text.\n"
                "Return ONLY a bullet-point list of terms.\n\n"
                f"{text}"
            )
        }
    ]

    response = ollama.chat(
        model='mistral:7b-instruct',
        messages=messages
    )

    terms = response['message']['content']

    return terms

