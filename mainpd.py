import pandas as pd
import json

# Load all sheets from the Excel file
excel_path = "two.xlsx"
sheets = pd.read_excel(excel_path, sheet_name=None)  # Load all sheets

questions_list = []

# Process each sheet
for sheet_name, df in sheets.items():
    print(f"📄 Processing sheet: {sheet_name}")  # Debugging info

    df = df.dropna(how="all")  # Remove fully empty rows

    question_data = {}
    options = {}

    for _, row in df.iterrows():
        label = str(row.iloc[0]).strip()
        text = str(row.iloc[1]).strip()

        if label.isdigit():  # New question
            if question_data:
                question_data["options"] = options
                questions_list.append(question_data)

            question_data = {"question": text, "options": {}, "answer": "", "marks": ""}
            options = {}

        elif label in ["A.", "B.", "C.", "D."]:
            options[label.strip(".")] = text

        elif "Answer" in label:
            question_data["answer"] = text

        elif "Marks" in label:
            question_data["marks"] = text

    if question_data:
        question_data["options"] = options
        questions_list.append(question_data)

# Save to JSON
json_path = "two.json"
with open(json_path, "w") as json_file:
    json.dump(questions_list, json_file, indent=4)

print(f"✅ Extracted data from all sheets and saved to {json_path}")

