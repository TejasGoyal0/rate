from fastapi import FastAPI
from app.models import OrdersRequest, OrderResponse
from app.rating_algorithm import StableReputation

app = FastAPI()
reputation_system = StableReputation()

@app.post("/update-score", response_model=list[OrderResponse])
def update_score(data: OrdersRequest):
    scores = []
    for order in data.transactions:
        new_score = reputation_system.update_score(order.order_value, order.returned)
        scores.append(OrderResponse(order_value=order.order_value, returned=order.returned, updated_score=new_score))
    
    return scores
