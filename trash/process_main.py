import re
import json
from PyPDF2 import PdfReader

# Define the path to your PDF file
pdf_path = "MAN22509.pdf"

# Initialize the PDF reader
reader = PdfReader(pdf_path)

# Extract text from the PDF
pdf_text = ""
for page in reader.pages:
    pdf_text += page.extract_text()

# Regex patterns to extract questions, options, and answers
question_pattern = re.compile(r"^\d+\s+(.*?)(?=\n[A-D]\.)", re.DOTALL)
options_pattern = re.compile(r"([A-D])\.\s+(.+?)(?=\n[A-D]\.|$)", re.DOTALL)
answer_pattern = re.compile(r"Answer\s+option([a-d])", re.IGNORECASE)

questions_data = []
current_question = None

# Process the extracted text line by line
lines = pdf_text.splitlines()
for line in lines:
    q_match = question_pattern.search(line)
    if q_match:
        # Save the previous question
        if current_question:
            questions_data.append(current_question)
        
        # Start a new question
        current_question = {"question": q_match.group(1).strip(), "options": {}, "answer": ""}
    
    # Add options to the current question
    if current_question:
        o_matches = options_pattern.findall(line)
        for o in o_matches:
            current_question["options"][o[0]] = o[1].strip()
    
    # Add the answer to the current question
    a_match = answer_pattern.search(line)
    if a_match and current_question:
        current_question["answer"] = a_match.group(1).upper()

# Append the last question
if current_question:
    questions_data.append(current_question)

# Save the extracted data to a JSON file
output_path = "questions_MAN22509.json"
with open(output_path, "w") as file:
    json.dump(questions_data, file, indent=2)

print(f"Questions have been extracted and saved to {output_path}")

