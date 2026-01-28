import re
from collections import defaultdict
from openai import OpenAI
import os
from dotenv import load_dotenv
from tqdm import tqdm
import ast

load_dotenv()

GPT_OSS_ENDPOINT = os.getenv("GPT_OSS_ENDPOINT")

def clean_extracted_terms(terms):

    
    # removes extra dashes and spaces
    removed_dashes = [term.strip("- ").strip() for term in terms if term.strip()]

    removed_leading_numbers = [strip_leading_numbers(term) for term in removed_dashes]

    removed_stars = [strip_leading_trailing_stars(term) for term in removed_leading_numbers]

    # lowercases all terms
    lower_case_terms = [term.lower() for term in removed_stars]

    # removes duplicates
    cleaned_terms = list(set(lower_case_terms))

    cleaned_terms.sort()

    print(f"Cleaned {len(terms)} terms to {len(cleaned_terms)} unique terms.")

    return cleaned_terms


def strip_leading_numbers(text: str) -> str:
    return re.sub(r'^\s*\d+\.\s*', '', text, flags=re.MULTILINE)

def strip_leading_trailing_stars(text: str) -> str:
    return re.sub(r'^\*+|\*+$', '', text, flags=re.MULTILINE)

def split_by_alphabet(words):
    groups = defaultdict(list)
    for word in words:
        if word:  # skip empty strings
            groups[word[0].upper()].append(word)
    return dict(groups)

def semantic_matching(terms, use_case, output_file):

    concepts = []

    # groups the terms by alphabetical order
    grouped_terms = split_by_alphabet(terms)

    # calls openrouter API
    client = OpenAI(
        base_url=GPT_OSS_ENDPOINT,
        api_key="dummy-key"
    )
    print(f"size of terms {len(terms)}")
    # print(f"grouped_terms {grouped_terms}")    

    for letter in tqdm(grouped_terms):

        # API call semantic matching canonical concepts
        response = client.chat.completions.create(
                model="gpt-oss:120b",
                messages=[
                    {"role": "system", "content":
                    "You are a clinical terminology normalization and relevance-filtering expert. "
                    "You specialize in cardiovascular disease concepts from clinical guidelines. "
                    "You normalize raw extracted terms into a minimal set of canonical concepts. "
                    "A canonical concept is the most standard, widely accepted clinical term "
                    "(e.g., 'Atrial Fibrillation', not 'AF', 'atrial fib', or 'AF (paroxysmal)'). "
                    "You merge synonyms, spelling variants, abbreviations, and minor wording differences. "
                    "You do NOT invent new concepts. "
                    "You MUST filter concepts based on the provided use case and exclude any concept "
                    "that is not directly relevant to fulfilling the use case objective."
                    },
                    {"role": "user", "content":
                    f"""
                    Use Case:
                    {use_case}

                    Definition of relevance:
                    A concept is relevant ONLY IF it directly supports, informs, diagnoses,
                    monitors, stratifies risk for, or guides treatment related to the use case.

                    Extracted terms from clinical guidelines:
                    {grouped_terms[letter]}

                    Task:
                    1. Normalize and merge synonymous or equivalent terms.
                    2. Resolve abbreviations into their full canonical form.
                    3. Remove qualifiers such as severity, timing, or measurement details
                    unless they define a distinct disease entity.
                    4. FILTER the concepts so that ONLY those relevant to the use case remain.
                    5. Exclude all other cardiovascular concepts, even if they are valid in general.

                    Output format:
                    - Return a Python-style list of strings
                    - One canonical concept per item
                    - No explanations, no duplicates, no numbering
                    - Return an empty list [] if no concepts satisfy the use case
                    """
                    }
                ]
        )

        response = response.choices[0].message

        canonical_terms = response.content
        print(f"Canonical terms for letter {letter} are\n{canonical_terms}")

        list_of_canonical_terms = ast.literal_eval(canonical_terms)

        concepts.extend(list_of_canonical_terms)

    # opens the output file to write canonical concepts
    with open(output_file, "w", encoding="utf-8") as f:
        for concept in concepts:
            f.write(f"{concept}\n")
