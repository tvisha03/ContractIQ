import re

def detect_pain_points(text: str, contract_type: str) -> list:
    pain_points = []

    rules = [
        {
            "pattern": r"unlimited liability",
            "issue": "Unlimited liability exposure",
            "type": "high_risk"
        },
        {
            "pattern": r"automatic renewal(?!.*30\s+days)",
            "issue": "Auto-renewal without 30-day exit clause",
            "type": "medium_risk"
        },
        {
            "pattern": r"non[-\s]?compete",
            "issue": "Non-compete clause",
            "type": "medium_risk",
            "contract_type": "employment"
        },
        {
            "pattern": r"termination.*without.*notice",
            "issue": "Termination without sufficient notice",
            "type": "high_risk"
        },
        {
            "pattern": r"no liability",
            "issue": "No liability clause (may protect one side unfairly)",
            "type": "medium_risk"
        }
    ]

    for rule in rules:
        if "contract_type" in rule and rule["contract_type"] != contract_type:
            continue  # skip rules not relevant to current type

        matches = re.finditer(rule["pattern"], text, re.IGNORECASE)
        for match in matches:
            pain_points.append({
                "type": rule["type"],
                "issue": rule["issue"],
                "start": match.start(),
                "end": match.end()
            })

    return pain_points
