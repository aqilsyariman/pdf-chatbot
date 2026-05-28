import os
import PyPDF2
import uuid
import chromadb
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from langchain_groq import ChatGroq
import streamlit as st
load_dotenv()

groq_api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
os.environ["GROQ_API_KEY"] = groq_api_key
model = SentenceTransformer('all-MiniLM-L6-v2')

def validate_files(files):
    valid_files = []
    for file in files:
        if file.endswith(".pdf"):
            valid_files.append(file)
    return valid_files

def read_pdf(file_name):
    pdf_file = open(file_name,"rb")
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def split_text(text):
    chunks = []
    for i in range(0, len(text), 500):
        chunk = text[i:i+500]
        chunks.append(chunk)
    return chunks

def embed_chunks(chunks):
    vectors = model.encode(chunks)
    return vectors

def store_vectors(chunks, vectors):
    client = chromadb.Client()
    
    # Optional but recommended: Delete the old collection first 
    # so answers from an old PDF don't mix with a newly uploaded PDF!
    try:
        client.delete_collection("pdf_chunks")
    except Exception:
        pass
        
    collection = client.create_collection("pdf_chunks") 
    
    ids = []
    for i in range(len(chunks)):
        # Generate a guaranteed unique random ID for every chunk
        ids.append(str(uuid.uuid4()))
        
    collection.add(
        embeddings=vectors,
        documents=chunks,
        ids=ids
    )
    return collection

def search(question, collection):
    question_vector = model.encode(question)
    results = collection.query(
        query_embeddings=[question_vector.tolist()],
        n_results=3
    )
    if not results['documents'] or not results['documents'][0]:
        return None
    return results

def get_answer(question, results):
    llm = ChatGroq(model="llama-3.1-8b-instant")
    context = " ".join(results['documents'][0])
    prompt = f"Based on this information: {context} Answer this question: {question}"
    answer = llm.invoke(prompt)
    return answer.content

if __name__ == "__main__":
    result = validate_files(["data/L1 IP (added subnet route).pdf"])
    if result:
        text = read_pdf(result[0])
        chunks = split_text(text)
        vectors = embed_chunks(chunks)
        collection = store_vectors(chunks, vectors.tolist())
        print("Stored in ChromaDB!!")
        question = input("Ask a question about your PDF: ")
        results = search(question, collection)
        if results is None:
            print("Sorry, I cannot find relevant information in this PDF")
        else:
            final_answer = get_answer(question, results)
            print(final_answer)