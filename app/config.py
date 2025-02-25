class Config:
    MAX_TRANSACTIONS = 50  # Transactions considered in scoring
    BASE_REWARD = 0.66  # Base reward for successful order
    BASE_PENALTY = -2  # Base penalty for return
    VALUE_FACTOR = 0.0005  # Multiplier for order value impact
    MIN_SCORE = -10
    MAX_SCORE = 10
