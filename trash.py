'''
#import pandas as pd

#excel_path = "one.xlsx"
#df = pd.read_excel(excel_path)
#print(df.columns.tolist())

import pandas as pd

excel_path = "one.xlsx"
sheets = pd.ExcelFile(excel_path)
print(sheets.sheet_names)
for sheet in sheets.sheet_names:
    df = pd.read_excel(excel_path, sheet_name=sheet)
    print(f"\n📄 Sheet: {sheet}")
    print(df.head())


for sheet in sheets.sheet_names:
    df = pd.read_excel(excel_path, sheet_name=sheet)
    print(f"\n📄 Sheet: {sheet} - Columns: {df.columns.tolist()}")
'''



import pandas as pd
import json

excel_path = "one.xlsx"
sheets = pd.read_excel(excel_path, sheet_name=None)

questions_list = []

for sheet_name, df in sheets.items():
    df = df.dropna(how="all")
    df = df.applymap(lambda x: x.encode('latin1').decode('utf-8', 'ignore') if isinstance(x, str) else x)  # Fix encoding

    question_data = {}
    options = {}

    for _, row in df.iterrows():
        label = str(row.iloc[0]).strip()
        text = str(row.iloc[1]).strip()

        if label.isdigit():
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

with open("onet.json", "w", encoding="utf-8") as json_file:
    json.dump(questions_list, json_file, indent=4, ensure_ascii=False)

print("✅ Done! Check 'question_details.json'")

