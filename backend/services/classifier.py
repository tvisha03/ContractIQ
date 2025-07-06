def classify_contract(text: str) -> str:
    text = text.lower()

    # Define keyword buckets
    nda_keywords = ["non-disclosure", "confidential", "proprietary information", 
                    "trade secret", "confidentiality agreement"]

    employment_keywords = ["employment agreement", "offer letter", "employee handbook",
                          "salary", "benefits", "termination", "at-will employment"]

    investment_keywords = ["term sheet", "convertible note", "equity", "shares",
                          "investment agreement", "valuation", "liquidation preference"]

    services_keywords = ["statement of work", "master service agreement", "consulting",
                        "deliverables", "scope of work", "professional services"]

    # Scoring logic
    scores = {
        "nda": sum(1 for keyword in nda_keywords if keyword in text),
        "employment": sum(1 for keyword in employment_keywords if keyword in text),
        "investment": sum(1 for keyword in investment_keywords if keyword in text),
        "services": sum(1 for keyword in services_keywords if keyword in text)
    }

    # Return highest scoring category or "other"
    return max(scores, key=scores.get) if max(scores.values()) > 0 else "other"
