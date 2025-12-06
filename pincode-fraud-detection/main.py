from fastapi import FastAPI
from pydantic import BaseModel
import pinecone
from sentence_transformers import SentenceTransformer
import numpy as np

app = FastAPI(title="Fraud Detection API (Pinecone-Based)")

# Initialize model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Initialize Pinecone
pc = pinecone.Pinecone(api_key="YOUR_PINECONE_API_KEY")
index = pc.Index("fraud-transactions")

class Transaction(BaseModel):
    transaction_id: str
    sender: str
    receiver: str
    amount: float
    timestamp: str
    location: str = "Unknown"
    fraud_flag: bool | None = None

def serialize_transaction(tx):
    return (
        f"Transaction from {tx.sender} to {tx.receiver} "
        f"for amount {tx.amount} at {tx.timestamp} in {tx.location}."
    )

def get_embedding(text):
    return model.encode([text])[0].tolist()

@app.post("/score")
def score_transaction(tx: Transaction):
    doc = serialize_transaction(tx)
    emb = get_embedding(doc)

    results = index.query(vector=emb, top_k=5, include_metadata=True)
    fraud_score = max([m.score for m in results.matches if m.metadata.get("fraud_flag")], default=0)

    return {
        "transaction_id": tx.transaction_id,
        "fraud_score": fraud_score,
        "label": "fraud" if fraud_score > 0.75 else "suspicious" if fraud_score > 0.45 else "clean",
        "matches": results.matches
    }

@app.post("/ingest")
def ingest_transaction(tx: Transaction):
    doc = serialize_transaction(tx)
    emb = get_embedding(doc)

    index.upsert([
        {"id": tx.transaction_id, "values": emb, "metadata": tx.dict()}
    ])

    return {"status": "success", "id": tx.transaction_id}