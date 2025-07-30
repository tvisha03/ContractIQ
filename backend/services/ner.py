import spacy
from spacy.lang.en import English

# --- 1. Load the Transformer Model ---
# This is a large, powerful model. It might take a moment to load the first time.
try:
    nlp = spacy.load("en_core_web_trf")
    print("spaCy transformer model 'en_core_web_trf' loaded successfully.")
except OSError:
    print("Could not find 'en_core_web_trf'. Please run 'python -m spacy download en_core_web_trf'")
    # Fallback to a blank model if the transformer isn't available
    nlp = English()


# --- 2. Create the Rule-Based EntityRuler ---
# You can keep adding specific, high-precision rules here.
ruler = nlp.add_pipe("entity_ruler", before="ner")
patterns = [
    {"label": "PHONE_NUMBER", "pattern": [{"TEXT": {"REGEX": r"(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})"}}]},
    {"label": "EMAIL_ADDRESS", "pattern": [{"LIKE_EMAIL": True}]}
]
ruler.add_patterns(patterns)


def extract_contract_entities(text: str) -> list:
    """
    Extracts entities from contract text using a hybrid approach:
    1. A pre-trained transformer model for general entities (PERSON, ORG, etc.).
    2. A rule-based system for specific patterns (phone numbers, emails).
    """
    if not nlp:
        return []

    doc = nlp(text)

    # We'll use a set to avoid duplicate entities
    unique_entities = set()

    # Extract entities and add them to our set
    for ent in doc.ents:
        # We can ignore certain labels if they are not useful
        if ent.label_ not in ["CARDINAL", "DATE"]:
            unique_entities.add((ent.text.strip(), ent.label_))

    # Convert the set of tuples to a list of dictionaries for the final output
    entities_list = [{"text": text, "label": label} for text, label in unique_entities]

    return entities_list
