import PyPDF2

# ALL functions at top
def validate_files(files):
    valid_files = []
    for file in files:
        if file.endswith(".pdf"):
            valid_files.append(file)
    return valid_files

def read_pdf(file_name):
    pdf_file = open(file_name,"rb")
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""          # ← missing
    for page in reader.pages : 
        text += page.extract_text()  # ← needs indent
    return text

def split_text(text):
    chunks = []
    for i in range(0, len(text), 500):
        chunk = text[i:i+500]
        chunks.append(chunk)
    return chunks

# ALL calls at bottom
result = validate_files(["L1 IP (added subnet route).pdf"])

if result:
    text = read_pdf(result[0])
    chunks = split_text(text)
    print(f"Total chunks: {len(chunks)}")
else:
    print("Error: Not a PDF file")
    
