# PDF Question Answering Chatbot

A RAG (Retrieval-Augmented Generation) system that allows you to ask questions about any PDF document and get accurate AI-powered answers — with built-in hallucination prevention.

## What It Does

Place any PDF file in the project folder and ask questions about its content. The system reads the document, understands the meaning of each section, and returns precise answers based only on the information inside the PDF.

If you ask something unrelated to the PDF, the system will tell you it cannot find relevant information — instead of making up an answer.

**Example:**
```
Ask a question about your PDF: What is ICMP?
Answer: ICMP stands for Internet Control Message Protocol. It handles error 
and control messages in IP networks. If a router cannot deliver a packet, 
it sends an ICMP host unreachable message back to the source...

Ask a question about your PDF: What is the recipe for nasi lemak?
Answer: Sorry, I cannot find relevant information in this PDF.
```

## How It Works

```
PDF → Validate → Read all pages → Split into chunks → Convert to vectors → Store in ChromaDB → User asks question → Search by meaning → AI answers
```

1. Validates the uploaded file is a PDF
2. Extracts text from every page
3. Splits text into 500-character chunks
4. Converts each chunk into vectors using Sentence Transformers
5. Stores vectors in ChromaDB vector database
6. Converts user question into a vector
7. Finds the most semantically relevant chunks
8. Rejects irrelevant questions using distance threshold
9. Sends relevant chunks to AI to generate a clear answer

## Tech Stack

- **Python** — Core language
- **PyPDF2** — PDF text extraction
- **Sentence Transformers** — Text to vector conversion
- **ChromaDB** — Vector database storage and search
- **LangChain** — AI model integration
- **Groq API** — Free AI inference (LLaMA 3.1)

## Installation

### Prerequisites
- Python 3.10+
- VSCode
- Mac or Windows

### Step 1 — Clone the repository
```bash
git clone https://github.com/aqilsyariman/pdf-chatbot.git
cd pdf-chatbot
```

### Step 2 — Install dependencies
```bash
pip3 install PyPDF2 sentence-transformers chromadb langchain langchain-groq
```

### Step 3 — Get a free Groq API key
1. Go to [console.groq.com](https://console.groq.com)
2. Sign up for free — no credit card needed
3. Create an API key

### Step 4 — Set your API key
```bash
export GROQ_API_KEY="your-api-key-here"
```

### Step 5 — Add your PDF
Place your PDF file in the project folder and update this line in `chatbot.py`:
```python
result = validate_files(["your-file.pdf"])
```

### Step 6 — Run
```bash
python3 chatbot.py
```

### Step 7 — Ask anything
```
Ask a question about your PDF: your question here
```

## Features

- Accepts any text-based PDF
- Reads all pages automatically
- Interactive question input — no hardcoding needed
- Semantic search — finds answers by meaning, not just keywords
- Hallucination prevention — rejects questions not related to the PDF
- Free to run — uses Groq free tier

## Project Structure

```
pdf-chatbot/
│
├── chatbot.py       # Main application
└── README.md        # Documentation
```

## Built By

Aqil Syariman — AI Engineer in progress 🔥
