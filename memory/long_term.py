import chromadb
from uuid import uuid4

client = chromadb.HttpClient(
    host="localhost",
    port=8000,
    ssl=False,
    headers=None
)

collection = client.get_or_create_collection("long_term_memory")

def save_memory(text):
    collection.add(
        documents=[text],
        ids=[str(uuid4())]
    )

def query_memory(query, n_results=3, max_score=0.7):
    results = collection.query(
        query_texts=[query],
        n_results=n_results,
        include=["documents", "distances"]
    )

    documents = []
    if results["documents"]:
        for doc, score in zip(results["documents"][0], results["distances"][0]):
            if score <= max_score:
                documents.append(doc)
    return documents

def get_all_memories():
    return collection.get()