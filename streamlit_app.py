import streamlit as st
from app import validate_files, read_pdf, split_text, embed_chunks, store_vectors, search, get_answer

st.title("Ask My PDF powered by RAG Assistant")
st.write("Upload a PDF and ask questions about it")

uploaded_file = st.file_uploader("Upload your PDF", type="pdf")
question = st.text_input("Ask a question about your PDF")

if st.button("Ask"):
    if uploaded_file and question:
        # save temp file
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.read())
        
        text = read_pdf("temp.pdf")
        split = split_text(text)
        embed = embed_chunks(split)
        collection = store_vectors(split,embed.tolist())
        results = search(question,collection)
        answer = get_answer(question,results)
        st.write(answer)
        
        