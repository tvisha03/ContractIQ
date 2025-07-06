import spacy
from spacy.pipeline import EntityRuler

nlp = spacy.load("en_core_web_sm")
ruler = nlp.add_pipe("entity_ruler", before="ner", config={"overwrite_ents": True})

patterns = [
    {"label": "DISCLOSING_PARTY", "pattern": [{"LOWER": "party"}, {"LOWER": "disclosing"}, {"LOWER": "information"}]},
    {"label": "RECEIVING_PARTY", "pattern": [{"LOWER": "party"}, {"LOWER": "receiving"}, {"LOWER": "information"}]},
    {"label": "CONFIDENTIAL_INFO", "pattern": [{"LOWER": "confidential"}, {"LOWER": "information"}]},
    {"label": "EXCLUSION_CRITERIA", "pattern": [{"LOWER": "publicly"}, {"LOWER": "known"}]},
    {"label": "RETENTION_PERIOD", "pattern": [{"LOWER": "shall"}, {"LOWER": "remain"}, {"LOWER": "in"}, {"LOWER": "effect"}, {"LOWER": "until"}]},
    {"label": "IMMUNITY_NOTICE", "pattern": [{"LOWER": "notice"}, {"LOWER": "of"}, {"LOWER": "immunity"}]},
]

ruler.add_patterns(patterns)

def extract_contract_entities(text: str):
    doc = nlp(text)
    allowed_labels = {
        "DISCLOSING_PARTY", "RECEIVING_PARTY", "CONFIDENTIAL_INFO",
        "EXCLUSION_CRITERIA", "RETENTION_PERIOD", "AGREEMENT_DATE", "IMMUNITY_NOTICE"
    }
    return [{"text": ent.text.strip(), "label": ent.label_} for ent in doc.ents if ent.label_ in allowed_labels]
