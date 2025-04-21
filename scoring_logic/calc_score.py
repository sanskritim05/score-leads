import csv
from scoring_logic.database import db


#calculate total possible score
def calculate_max_score():
    max_score = 0
    for question, answers in db.items():
        if "(Select all that apply)" in question:
            max_score += sum(answers.values())
        else:
            max_score += max(answers.values())
    return max_score

#normalizes spacing and formatting for header
def normalize_header(header):
    return header.strip().replace("\xa0", " ").replace("\n", " ").strip()

#normalizes cell value
def normalize_value(value):
    return value.strip().replace("\xa0", " ").replace("\n", " ").strip().lower()

#match user answer to answer
def match_answer(option, answer_map):
    for key in answer_map:
        if normalize_value(key) == option:
            return answer_map[key]
    return 0

#process CSV and give score
def findScores(file_path):
    results = []
    true_max_score = calculate_max_score()

    with open(file_path, 'r', encoding='utf-8-sig') as file:
        csv_reader = csv.DictReader(file)
        field_map = {normalize_header(h): h for h in csv_reader.fieldnames}

        for row in csv_reader:
            score = 0
            first_name = row.get(field_map.get("First Name", ""), "").strip()
            last_name = row.get(field_map.get("Last Name", ""), "").strip()
            client_name = f"{first_name} {last_name}".strip() or "Unknown"

            for db_question, answer_map in db.items():
                normalized_q = normalize_header(db_question)
                csv_key = next((k for k in field_map if normalized_q in normalize_header(k)), None)
                if not csv_key:
                    continue

                response = row.get(field_map[csv_key], "")
                if not response:
                    continue
                response = normalize_value(response)

                if "(Select all that apply)" in db_question:
                    selected_options = [normalize_value(opt) for opt in response.split(";") if opt.strip()]
                    for option in selected_options:
                        score += match_answer(option, answer_map)
                else:
                    score += match_answer(response, answer_map)

            results.append({
                "Client Name": client_name,
                "Score": score,
                "Max Score": true_max_score
            })

    return results
