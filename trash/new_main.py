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

# Prepare for extracting questions, options, and answers
questions_data = []
question = None
options = {}
answer = None

# Regular expressions
question_regex = re.compile(r"^\d+\s+(.*?)(?=\n[A-D]\.)", re.DOTALL)
options_regex = re.compile(r"([A-D])\.\s+(.+)")
answer_regex = re.compile(r"Answer\s+option([A-Da-d])", re.IGNORECASE)

# Parse the text
lines = pdf_text.split("\n")
for line in lines:
    # Check for a new question
    q_match = question_regex.match(line)
    if q_match:
        # Save the previous question
        if question and options and answer:
            questions_data.append({
                "question": question.strip(),
                "options": options,
                "answer": answer.upper(),
            })
        # Reset for the next question
        question = q_match.group(1)
        options = {}
        answer = None

    # Check for options
    if options_regex.match(line):
        o_match = options_regex.findall(line)
        for opt in o_match:
            options[opt[0]] = opt[1].strip()

    # Check for an answer
    a_match = answer_regex.search(line)
    if a_match:
        answer = a_match.group(1).upper()

# Append the last question
if question and options and answer:
    questions_data.append({
        "question": question.strip(),
        "options": options,
        "answer": answer.upper(),
    })

# Save the extracted data to a JSON file
output_path = "questions_MAN22509.json"
with open(output_path, "w") as file:
    json.dump(questions_data, file, indent=2)

print(f"Questions extracted and saved to {output_path}")

