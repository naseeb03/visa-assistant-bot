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
collection = client.get_collection("visa_documents")

embedder = SentenceTransformer('all-MiniLM-L6-v2')

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
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
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
