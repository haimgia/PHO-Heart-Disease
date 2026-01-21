import pymupdf
from openai import OpenAI
from tqdm import tqdm
from dotenv import load_dotenv
import os

load_dotenv()

OPEN_ROUTER_API_KEY = os.getenv("OPEN_ROUTER_API_KEY")

def extract_text(pdf_file):
    doc = pymupdf.open(pdf_file) # open a document
    #out = open("output.txt", "wb") # create a text output
    for i, page in tqdm(enumerate(doc)): # iterate the document pages
        text = page.get_text().encode("utf8") # get plain text (is in UTF-8)

        terms = extract_concepts(text.decode('utf8'))
        print(f"Extracted terms from page {i + 1}:\n {terms}\n")

        #out.write(text) # write text of page
        #out.write(bytes((12,))) # write page delimiter (form feed 0x0C)
    #out.close()

def extract_concepts(text):
    # Placeholder for concept extraction logic
    concepts = []

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPEN_ROUTER_API_KEY,
    )

    # First API call to extract concepts
    response = client.chat.completions.create(
    model="openai/gpt-oss-120b:free",
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