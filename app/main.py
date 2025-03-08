from fastapi import FastAPI
from models import OrdersRequest
from ratingAlgorithm import calculate_reputation

app = FastAPI()

@app.post("/update-score")
def update_score(data: OrdersRequest):
    # Convert transactions to list of dicts
    transactions = [order.dict() for order in data.transactions]
    reputation = calculate_reputation(transactions)
    return {"reputation": reputation}

# To run: uvicorn main:app --host 0.0.0.0 --port $PORT

