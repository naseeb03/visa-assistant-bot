import chromadb
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

load_dotenv()

client = chromadb.PersistentClient(path="db")

collection = client.create_collection(name="visa_documents")

embedder = SentenceTransformer('all-MiniLM-L6-v2')

def chunk_documents(doc, chunk_size=500):
    """
    Splits the text of a document into chunks of a given size.
    """
    chunks = []
    for i in range(0, len(doc), chunk_size):
        chunks.append(doc[i:i + chunk_size])
    return chunks

def add_chunks_to_db(chunks, collection_name):
    """
    Adds document chunks to the Chromadb collection with embeddings.
    """
    embeddings = embedder.encode(chunks)

    for idx, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        collection.add(
            documents=[chunk],
            metadatas=[{"source": collection_name}],
            ids=[f"{collection_name}_chunk_{idx}"],
            embeddings=[embedding]
        )

def process_and_store_files():
    with open("data/visa_spain_dnv.txt", "r") as file:
        spain_doc = file.read()
    spain_chunks = chunk_documents(spain_doc)
    add_chunks_to_db(spain_chunks, "visa_spain")

    with open("data/visa_albania_residency.txt", "r") as file:
        albania_doc = file.read()
    albania_chunks = chunk_documents(albania_doc)
    add_chunks_to_db(albania_chunks, "visa_albania")
    
process_and_store_files()

print("Chunks have been successfully added to Chromadb.")
