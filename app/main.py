from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import numpy as np

# Define Pydantic models inline
class Order(BaseModel):
    order_value: int
    returned: bool

class OrdersRequest(BaseModel):
    transactions: List[Order]

# Rating algorithm (stateless)
def calculate_reputation(
    transactions: List[dict],
    max_transactions: int = 50,
    base_reward: float = 0.66,
    base_penalty: float = -2,
    value_factor: float = 0.0005
):
    """
    Calculate a reputation score based on a list of transactions.
    Each transaction should have:
      - order_value (int)
      - returned (bool)
    Only the most recent 'max_transactions' are considered.
    The final reputation is normalized to a value between 0 and 10.
    """
    # Consider only the most recent transactions
    transactions = transactions[-max_transactions:]
    
    contributions = []
    for t in transactions:
        if t["returned"]:
            contributions.append(base_penalty * (1 + value_factor * t["order_value"]))
        else:
            contributions.append(base_reward + (value_factor * t["order_value"]))
    
    raw_score = sum(contributions)
    
    # Define hard limits for normalization
    min_score, max_score = -10, 10
    normalized = ((raw_score - min_score) / (max_score - min_score)) * 10
    rating = np.clip(normalized, 0, 10)
    
    return round(rating, 2)

# Create FastAPI app
app = FastAPI()

@app.post("/update-score")
def update_score(data: OrdersRequest):
    # Convert transactions to list of dicts
    transactions = [order.dict() for order in data.transactions]
    reputation = calculate_reputation(transactions)
    return {"reputation": reputation}

# To run locally, use:
# uvicorn main:app --host 0.0.0.0 --port 8000


