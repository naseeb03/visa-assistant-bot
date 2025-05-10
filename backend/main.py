from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import requests
import chromadb
from sentence_transformers import SentenceTransformer

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_origin_regex="http://.*",
)

client = chromadb.PersistentClient(path="db")
collection = client.get_or_create_collection("visa_documents")
embedder = SentenceTransformer('all-MiniLM-L6-v2')

def chunk_documents(doc, chunk_size=500):
    chunks = []
    for i in range(0, len(doc), chunk_size):
        chunks.append(doc[i:i + chunk_size])
    return chunks

def add_chunks_to_db(chunks, collection_name):
    embeddings = embedder.encode(chunks)
    for idx, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        collection.add(
            documents=[chunk],
            metadatas=[{"source": collection_name}],
            ids=[f"{collection_name}_chunk_{idx}"],
            embeddings=[embedding]
        )

def process_and_store_files():
    existing_ids = collection.get()["ids"]
    if any("visa_spain" in id for id in existing_ids) and any("visa_albania" in id for id in existing_ids):
        print("Data already exists in ChromaDB. Skipping processing.")
        return

    with open("data/visa_spain_dnv.txt", "r") as file:
        spain_doc = file.read()
    spain_chunks = chunk_documents(spain_doc)
    add_chunks_to_db(spain_chunks, "visa_spain")

    with open("data/visa_albania_residency.txt", "r") as file:
        albania_doc = file.read()
    albania_chunks = chunk_documents(albania_doc)
    add_chunks_to_db(albania_chunks, "visa_albania")

    print("Chunks have been successfully added to ChromaDB.")

@app.on_event("startup")
async def startup_event():
    process_and_store_files()

class Query(BaseModel):
    question: str

@app.post("/ask")
async def answer_question(query: Query):
    user_question = query.question
    query_embedding = embedder.encode(user_question).tolist()
    results = collection.query(query_embeddings=[query_embedding], n_results=3)
    context_chunks = results["documents"][0]
    distances = results["distances"][0]
    context = "\n\n".join(context_chunks)

    if any(distance < 1 for distance in distances):
        prompt = f"""You are a visa and immigration assistant.
Based strictly on the following context from official immigration documents, answer the question clearly and concisely. Do not add extra information or assumptions. Only use facts provided in the context.

Context:
{context}

Question: {user_question}
Give a precise answer:"""
    else:
        prompt = f"""You are a visa and immigration assistant. Based on your general knowledge, please answer the following question:

Question: {user_question}
Give a precise answer:"""

    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash:generateContent?key={API_KEY}"
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        gemini_reply = response.json()['candidates'][0]['content']['parts'][0]['text']
        return {"answer": gemini_reply}
    else:
        return {
            "error": "Failed to get response from Gemini API",
            "status_code": response.status_code,
            "details": response.text
        }

@app.get("/")
def read_root():
    return {"message": "Visa & Immigration Assistant API is running!"}