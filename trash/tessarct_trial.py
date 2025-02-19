from pdf2image import convert_from_path
import pytesseract

pdf_path = "MAN22509.pdf"
images = convert_from_path(pdf_path)

text = ""
for img in images:
    text += pytesseract.image_to_string(img)

with open("ocr_extracted_text.txt", "w") as f:
    f.write(text)

print("OCR text saved to ocr_extracted_text.txt")

