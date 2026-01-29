from openai import OpenAI
import os
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()

GPT_OSS_ENDPOINT = os.getenv("GPT_OSS_ENDPOINT")

def generate_definitions(terms, output_file):

    definitions = []

    # calls openrouter API
    client = OpenAI(
        base_url=GPT_OSS_ENDPOINT,
        api_key="dummy-key"
    )
    #print(f"size of terms {len(terms)}")
    # print(f"grouped_terms {grouped_terms}")    

    for term in tqdm(terms):

        # API call semantic matching canonical concepts
        response = client.chat.completions.create(
                model="gpt-oss:120b",
                messages=[
                    {"role": "system", "content":
                    """
                    You are a clinical terminology expert specializing in cardiovascular and heart disease domains.
                    Your task is to generate concise, precise, and clinically grounded definitions suitable for
                    medical knowledge bases, ontologies, and decision-support systems.

                    Definitions must:
                    - Be specific to cardiovascular and heart disease contexts
                    - Use formal medical language
                    - Avoid casual phrasing, examples, or patient advice
                    - Not be circular
                    - Be 1–3 sentences in length
                    - Clearly distinguish the concept from related terms

                    If applicable, indicate whether the concept represents a disease, risk factor, biomarker,
                    clinical measurement, diagnostic test, or intervention, but do not include headings or labels
                    in the output—definition text only.
                    """
                    },
                    {"role": "user", "content":
                    f"""
                    Define the following concept for a heart disease–related use case:

                    Concept: {term}

                    Return only the definition text.
                    """
                    }
                ]
        )

        response = response.choices[0].message

        definition = response.content
        print(f"{term} - {definition}")

        definitions.append(f"{term} - {definition}")

    with open(output_file, "w", encoding="utf-8") as f:
        for definition in definitions:
            f.write(f"{definition}\n")
    