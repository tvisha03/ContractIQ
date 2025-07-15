import re
import json
import os

def detect_pain_points(text: str, contract_type: str) -> list:
    import logging
    from .pain_point_explanations import pain_point_explanations
    pain_points = []
    total_risk = 0
    max_possible = 0
    group_risks = {}
    group_points = {}
    log_matches = []

    # Section splitting regex (matches e.g. 'Section 1', '1.', '1.1', 'ARTICLE I', etc.)
    section_regex = re.compile(r'(Section|Clause|Article)?\s*(\d{1,2}(?:\.\d{1,2})*|[IVXLC]+)\.?\s+([A-Z][^\n\r]{0,80})', re.IGNORECASE)
    # Find all section headers and their positions
    sections = []
    for m in section_regex.finditer(text):
        sections.append({
            'title': m.group(0).strip(),
            'start': m.start(),
            'end': m.end()
        })
    # Add a dummy section at the end for easier slicing
    sections.append({'title': 'END', 'start': len(text), 'end': len(text)})

    # Load rules from JSON file
    rules_path = os.path.join(os.path.dirname(__file__), 'pain_points_rules.json')
    with open(rules_path, 'r') as f:
        rules = json.load(f)

    # Clause type mapping (for grouping)
    clause_map = {
        'termination': ['termination', 'notice', 'unilateral'],
        'compensation': ['salary', 'payment', 'compensate', 'rent'],
        'confidentiality': ['confidential', 'nda'],
        'liability': ['liability', 'waive'],
        'arbitration': ['arbitration', 'dispute'],
        'maintenance': ['maintenance', 'repairs'],
        'capital': ['capital', 'contribution'],
        'other': []
    }

    def get_clause_type(issue, pattern):
        for group, keywords in clause_map.items():
            for k in keywords:
                if k in issue.lower() or k in pattern.lower():
                    return group
        return 'other'

    # For each section, run pain point rules
    for i in range(len(sections)-1):
        section = sections[i]
        section_text = text[section['start']:sections[i+1]['start']]
        section_title = section['title']
        normalized_text = section_text.replace('\n', ' ').replace('\r', ' ')

        for rule in rules:
            # Contract type filtering
            if "contract_types" in rule and contract_type not in rule["contract_types"]:
                continue

            # Flexible regex: allow up to 50 chars between key terms (wildcards)
            pattern = rule["pattern"]
            flexible_pattern = re.sub(r"\\s+", r"[^\n]{0,50}", pattern)

            matches = list(re.finditer(flexible_pattern, normalized_text, re.IGNORECASE))
            base_score = rule.get("risk_score", 50)
            risk_type = rule["type"]
            weight = 1.5 if risk_type == "high_risk" else 1.0
            clause_type = get_clause_type(rule["issue"], pattern)

            for match in matches:
                score = base_score
                confidence = 0.8 if weight > 1.0 else 0.6
                # Context boost: if match is near a clause keyword, +10%
                window = 50
                snippet = normalized_text[max(0, match.start()-window):match.end()+window]
                for k in clause_map.get(clause_type, []):
                    if re.search(k, snippet, re.IGNORECASE):
                        score = int(score * 1.1)
                        confidence += 0.1
                        break
                match_text = match.group(0)
                # Contextual rule: check if section title contains relevant keyword
                contextually_relevant = any(k in section_title.lower() for k in clause_map.get(clause_type, []))
                if contextually_relevant:
                    score = int(score * 1.1)
                    confidence += 0.05
                # Why it's a concern
                why = pain_point_explanations.get(rule["issue"], "See contract clause for details.")
                # Only add pain points of high or medium risk
                if risk_type in ("high_risk", "medium_risk"):
                    pain_point = {
                        "type": rule["type"],
                        "issue": rule["issue"],
                        "risk_score": score,
                        "confidence": round(confidence, 2),
                        "clause_type": clause_type,
                        "match_text": match_text,
                        "start": section['start'] + match.start(),
                        "end": section['start'] + match.end(),
                        "section": section_title,
                        "why": why
                    }
                    pain_points.append(pain_point)
                    log_matches.append(pain_point)
                    # Grouping
                    group_points.setdefault(clause_type, []).append(pain_point)
                    group_risks[clause_type] = group_risks.get(clause_type, 0) + score * weight
                    total_risk += score * weight
                    max_possible += 100 * weight

    # Aggregate per-group risk levels (0-100)
    group_risk_levels = {g: round((v / (len(group_points[g])*100))*100, 1) if group_points[g] else 0 for g, v in group_risks.items()}
    # Calculate normalized risk score (0-100)
    risk_score = round((total_risk / max_possible) * 100, 1) if max_possible > 0 else 0.0

    # Log all matches for debugging
    logging.basicConfig(level=logging.INFO)
    logging.info(f"Pain point matches: {log_matches}")

    return pain_points, risk_score, group_risk_levels
