from extractor import extract_text
from cleaner import clean_extracted_terms, semantic_matching
from classifier import generate_definitions
import os

EXTRACT_TERMS = False
CLEAN_TERMS = False
SEMANTIC_MATCHING = False
DEFINING_CONCEPTS = True

#PDF = "AHA_clinical_guidelines\Heart Failure Clinical Guidelines.pdf"
CLINICAL_GUIDELINES_FOLDER = "AHA_clinical_guidelines"
TERMINOLOGY_FOLDER = "terminology"
EXTRACTED_TERMS_FOLDER = "extracted_terms_1.txt"
COMBINED_TERMS_FILE = "combined_extracted_terms.txt"
FINAL_TERMS_FILE = "canonical_terms_2.txt"
CANONICAL_TERMS_FILE = "canonical_terms_5.txt"
DEFINITIONS_FILE = "definitions.txt"

FINISHED_FILES = ["Acute Myocarditis Clinical Guidelines.pdf",
                  "Aortic Disease Clinical Guidelines.pdf",
                  "Chronic Coronary Disease Clinical Guidelines.pdf",
                  "Heart Failure Clinical Guidelines.pdf",
                  "Peripheral Artery Disease Clinical Guidelines.pdf",
                  "Primary Prevention of Cardiovascular Disease.pdf"]



USE_CASE = """
            Use Case Name: Anticipated Diagnosis for Heart Disease

            Goal: To inform a user whether they may be at elevated risk for heart disease and should seek evaluation by a medical professional before experiencing severe or acute symptoms (e.g., heart attack, heart failure, arrhythmia).
                This use case supports risk awareness and early intervention, not clinical diagnosis.

            Requirements: The anticipated diagnostic assessment considers:
                - Lifestyle factors: diet, physical activity, smoking, alcohol consumption, recreational drug use
                - Existing medical conditions: obesity, diabetes, hypertension, hyperlipidemia
                - Family medical history: presence of cardiovascular or related chronic diseases
                - Demographic background: age, sex, race, ethnicity
                Clinical reasoning and risk assessment should align with American Heart Association (AHA) guidelines and leverage standardized medical terminologies

            Scope: This use case primarily targets middle-aged and older adults (40+) in the United States, as this population is more likely to develop heart disease and aligns with AHA clinical guidelines.
                Out of scope:
                - Individuals already diagnosed with any form of heart disease
                - Clinical decision-making or definitive diagnosis
                - Emergency or acute care scenarios
                - Use by patients experiencing severe symptoms (e.g., chest pain, shortness of breath)
                While designed for U.S. adults aged 40+, individuals outside this demographic may still find the system useful for:
                - Preliminary risk awareness
                - Lifestyle guidance
                - Informational support prior to seeking medical advice

            Description: Heart disease is an umbrella term encompassing multiple conditions that affect heart function. In the United States, heart disease remains a leading cause of death, with many individuals remaining asymptomatic until a serious event occurs.
                Certain forms of heart disease are often “silent,” meaning individuals may not experience noticeable symptoms until the disease has significantly progressed. Common risk factors include increasing age, hypertension, high cholesterol, diabetes, obesity, smoking, physical inactivity, and poor diet. Additional factors such as sex, ethnicity, and family history further influence risk.
                This use case focuses on anticipated diagnosis, enabling users to recognize elevated risk early and seek medical evaluation before the onset of severe or irreversible outcomes. The ultimate objective is to promote earlier clinical engagement and healthier lifestyle choices.

            Usage Scenarios:
                1. A 52-year-old woman living in Baltimore, Maryland is preparing for an upcoming annual wellness visit but has not yet met with her primary care physician. She is not experiencing acute cardiovascular symptoms such as chest pain, shortness of breath at rest, or irregular heart rhythms. However, she is concerned about her long-term cardiovascular health due to a significant family history: her father was diagnosed with coronary artery disease in his late 50s, and her mother has type 2 diabetes. The user works a sedentary office job and exercises inconsistently. Her diet is high in processed foods, and although she quit smoking five years ago, she previously smoked socially for many years. She consumes alcohol occasionally. During a recent routine check-up, she was informed that her cholesterol levels were borderline high, and she has also been diagnosed with prediabetes but has not yet started medication.
                2. A 32-year-old man living in Austin, Texas begins experiencing intermittent fatigue and mild shortness of breath during physical activity that previously felt routine, such as climbing stairs or going for short runs. He does not report chest pain, dizziness, or symptoms severe enough to require emergency care, but he is concerned due to his family history of heart disease. His mother was diagnosed with coronary artery disease in her early 50s, and his maternal grandfather died of a heart attack. The user generally maintains an active lifestyle but works a high-stress job with long hours and inconsistent sleep. He does not smoke and drinks alcohol occasionally, though his diet relies heavily on takeout meals. He has not been diagnosed with any chronic conditions and has not undergone recent cardiovascular screening.

            Competency Questions:
                1. Refer to user scenario 1. Which risk factors most strongly contribute to an individual’s anticipated risk of heart disease based on current clinical guidelines?
                    Answer: Age (52 years old), family history (father diagnosed with coronary artery disease and mother has type 2 diabetes), diagnosis (prediabetic), high cholesterol, sedentary lifestyle, physical inactivity, unhealthy diet (high in processed foods), history of smoking (5 years ago), alcohol consumption (occasional)
                2. Refer to user scenario 2. Does the user’s strong family history of heart disease and mild exertional symptoms meet criteria for early cardiovascular screening?
                    Answer: Yes. The following factors contribute to recommended early cardiovascular screening: family history (mother’s premature diagnosis of coronary artery disease, maternal grandfather passing away of a heart attack),  mild symptoms (intermittent fatigue, mild shortness of breath in physical activity)
                3. Refer to user scenario 1. What are the vital signs the user is reporting?
                    Partial Answer: It depends on what is on the user’s EHR if they load it into the anticipated diagnostic assessment for heart disease
                4. Refer to usage scenario 2. What are the user’s lifestyle behaviors?
                    Answer: generally active, high-stress occupation, inconsistent sleep schedule, unhealthy diet (takeout meals), occasional consumption of alcohol
                5. Refer to usage scenario 1. What type of heart disease does this user have an elevated risk of?
                    Answer: atherosclerotic cardiovascular disease (ASCVD). Family history: father with coronary artery disease and mother with type 2 diabetes. High cholesterol. Prediabetic. Lifestyle factors: sedentary occupation, lack of exercise, unhealthy diet consisting of processed foods, and a history of smoking. Age (52 years old)
        """

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

    if SEMANTIC_MATCHING:
        with open(FINAL_TERMS_FILE, "r", encoding="utf-8") as f:
            terms = [line.strip() for line in f.readlines()]

        semantic_matching(terms, USE_CASE, CANONICAL_TERMS_FILE)

    if DEFINING_CONCEPTS:
        with open(os.path.join(TERMINOLOGY_FOLDER, CANONICAL_TERMS_FILE), "r", encoding="utf-8") as f:
            terms = [line.strip() for line in f.readlines()]

        generate_definitions(terms, DEFINITIONS_FILE)
