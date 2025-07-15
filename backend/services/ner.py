# --- NER LOGIC REWRITE BASED ON SUGGESTIONS ---
import spacy
import re
from spacy.pipeline import EntityRuler

nlp = spacy.load("en_core_web_sm", disable=["ner"])

def clean_contract(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    return text.replace("“", '"').replace("”", '"').strip()

# Remove existing entity ruler if any
if "entity_ruler" in nlp.pipe_names:
    nlp.remove_pipe("entity_ruler")

ruler = nlp.add_pipe("entity_ruler", before="ner", config={"overwrite_ents": True})


# --- Patterns ---
# Add more granular patterns for key-value fields
custom_patterns = [
    # Employer / Company
    {"label": "EMPLOYER", "pattern": [
        {"LOWER": "employer"}, {"TEXT": ":"}, {"IS_SPACE": True, "OP": "*"}, {"IS_TITLE": True, "OP": "+"}
    ]},
    {"label": "EMPLOYEE", "pattern": [
        {"LOWER": "employee"}, {"TEXT": ":"}, {"IS_SPACE": True, "OP": "*"}, {"IS_TITLE": True, "OP": "+"}
    ]},
    {"label": "INCORPORATION_STATE", "pattern": [
        {"LOWER": "incorporated"}, {"LOWER": "in"}, {"IS_TITLE": True, "OP": "+"}
    ]},
    {"label": "EFFECTIVE_DATE", "pattern": [
        {"LOWER": "effective"}, {"LOWER": "date"}, {"TEXT": ":"}, {"IS_SPACE": True, "OP": "*"}, {"IS_DIGIT": True, "OP": "+"}
    ]},
    {"label": "POSITION", "pattern": [
        {"LOWER": "position"}, {"TEXT": ":"}, {"IS_SPACE": True, "OP": "*"}, {"IS_TITLE": True, "OP": "+"}
    ]},
    {"label": "BASE_SALARY", "pattern": [
        {"LOWER": "base"}, {"LOWER": "salary"}, {"TEXT": ":"}, {"IS_SPACE": True, "OP": "*"}, {"IS_CURRENCY": True, "OP": "?"}, {"IS_DIGIT": True, "OP": "+"}
    ]},
    {"label": "WORKING_HOURS", "pattern": [
        {"LOWER": "working"}, {"LOWER": "hours"}, {"TEXT": ":"}, {"IS_SPACE": True, "OP": "*"}, {"IS_DIGIT": True, "OP": "+"}
    ]},
    {"label": "VACATION_DAYS", "pattern": [
        {"LOWER": "vacation"}, {"LOWER": "days"}, {"TEXT": ":"}, {"IS_SPACE": True, "OP": "*"}, {"IS_DIGIT": True, "OP": "+"}
    ]},
    {"label": "SICK_LEAVE", "pattern": [
        {"LOWER": "sick"}, {"LOWER": "leave"}, {"TEXT": ":"}, {"IS_SPACE": True, "OP": "*"}, {"IS_DIGIT": True, "OP": "+"}
    ]},
    {"label": "NON_COMPETE_DURATION", "pattern": [
        {"LOWER": "non-compete"}, {"LOWER": "duration"}, {"TEXT": ":"}, {"IS_SPACE": True, "OP": "*"}, {"IS_DIGIT": True, "OP": "+"}
    ]},
    {"label": "NON_COMPETE_RADIUS", "pattern": [
        {"LOWER": "non-compete"}, {"LOWER": "radius"}, {"TEXT": ":"}, {"IS_SPACE": True, "OP": "*"}, {"IS_DIGIT": True, "OP": "+"}
    ]},
    {"label": "CUSTOMER_SOLICITATION_BAN", "pattern": [
        {"LOWER": "customer"}, {"LOWER": "solicitation"}, {"LOWER": "ban"}, {"TEXT": ":"}, {"IS_SPACE": True, "OP": "*"}, {"IS_DIGIT": True, "OP": "+"}
    ]},
    {"label": "EMPLOYEE_SOLICITATION_BAN", "pattern": [
        {"LOWER": "employee"}, {"LOWER": "solicitation"}, {"LOWER": "ban"}, {"TEXT": ":"}, {"IS_SPACE": True, "OP": "*"}, {"IS_DIGIT": True, "OP": "+"}
    ]},
    {"label": "TERMINATION_NOTICE_EMPLOYER", "pattern": [
        {"LOWER": "termination"}, {"LOWER": "notice"}, {"LOWER": "employer"}, {"TEXT": ":"}, {"IS_SPACE": True, "OP": "*"}, {"IS_DIGIT": True, "OP": "+"}
    ]},
    {"label": "TERMINATION_NOTICE_EMPLOYEE", "pattern": [
        {"LOWER": "termination"}, {"LOWER": "notice"}, {"LOWER": "employee"}, {"TEXT": ":"}, {"IS_SPACE": True, "OP": "*"}, {"IS_DIGIT": True, "OP": "+"}
    ]},
    {"label": "ARBITRATION_AUTHORITY", "pattern": [
        {"LOWER": "arbitration"}, {"LOWER": "authority"}, {"TEXT": ":"}, {"IS_SPACE": True, "OP": "*"}, {"IS_TITLE": True, "OP": "+"}
    ]},
    {"label": "GOVERNING_LAW", "pattern": [
        {"LOWER": "governing"}, {"LOWER": "law"}, {"TEXT": ":"}, {"IS_SPACE": True, "OP": "*"}, {"IS_TITLE": True, "OP": "+"}
    ]},
    {"label": "IP_OWNERSHIP", "pattern": [
        {"LOWER": "intellectual"}, {"LOWER": "property"}, {"LOWER": "ownership"}, {"TEXT": ":"}, {"IS_SPACE": True, "OP": "*"}, {"IS_TITLE": True, "OP": "+"}
    ]},
    {"label": "SURVIVAL_CLAUSES", "pattern": [
        {"LOWER": "survival"}, {"LOWER": "clauses"}, {"TEXT": ":"}, {"IS_SPACE": True, "OP": "*"}, {"IS_TITLE": True, "OP": "+"}
    ]},
    # Add your previous patterns for parties, dates, signatures, etc.
]

# Add in sensible order: longest, most‑specific first
ruler.add_patterns(custom_patterns)

def extract_contract_entities(text: str):
    text = clean_contract(text)
    doc = nlp(text)
    # Include all custom entity labels and previous ones
    custom_labels = {p["label"] for p in custom_patterns}
    keep = custom_labels | {"PARTY", "DATE", "CONFIDENTIAL_INFO", "SIGNATORY", "EXCLUSION_CRITERIA", "RETENTION_PERIOD"}
    uniq = {}
    for e in doc.ents:
        if e.label_ in keep:
            # Get context window (30 chars before, 30 after)
            context_start = max(0, e.start_char - 30)
            context_end = min(len(doc.text), e.end_char + 30)
            context = doc.text[context_start:context_end].strip()
            # PARTY: split on colon to get role and value
            if e.label_ == "PARTY" and ":" in e.text:
                role, value = e.text.split(":", 1)
                uniq[(e.label_, role.strip(), e.start_char)] = {
                    "label": e.label_,
                    "text": e.text.strip(),
                    "role": role.strip(),
                    "value": value.strip(),
                    "start": e.start_char,
                    "end": e.end_char,
                    "context": context
                }
            # CONFIDENTIAL_INFO: try to grab info after the phrase
            elif e.label_ == "CONFIDENTIAL_INFO":
                after = text[e.end_char:e.end_char+80]
                info = after.split(".")[0].strip()
                uniq[(e.label_, e.text.strip(), e.start_char)] = {
                    "label": e.label_,
                    "text": e.text.strip(),
                    "info": info,
                    "start": e.start_char,
                    "end": e.end_char,
                    "context": context
                }
            else:
                uniq[(e.label_, e.text.strip(), e.start_char)] = {
                    "label": e.label_,
                    "text": e.text.strip(),
                    "start": e.start_char,
                    "end": e.end_char,
                    "context": context
                }
    return list(uniq.values())

# Example usage
if __name__ == "__main__":
    with open("sample_employment_contract.txt") as f:
        txt = clean_contract(f.read())
    for ent in extract_contract_entities(txt):
        print(f'{ent["label"]:10} | {ent["text"]}')
