from pydantic import BaseModel
from typing import List

class Order(BaseModel):
    order_value: int
    returned: bool

class OrdersRequest(BaseModel):
    transactions: List[Order]

class OrderResponse(BaseModel):
    order_value: int
    returned: bool
    updated_score: float
