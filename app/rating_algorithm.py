import numpy as np
from app.config import Config

class StableReputation:
    def __init__(self):
        self.score = 5.0  # Start at mid-point (0-10 scale)
        self.transaction_history = []  # Stores last N transactions

    def calculate_penalty(self, order_value):
        """Penalty increases with order value."""
        return Config.BASE_PENALTY * (1 + Config.VALUE_FACTOR * order_value)

    def calculate_reward(self, order_value):
        """Reward increases with order value."""
        return Config.BASE_REWARD + (Config.VALUE_FACTOR * order_value)

    def update_score(self, order_value, returned):
        """Updates reputation score considering order value & return status."""
        if returned:
            penalty = self.calculate_penalty(order_value)
            self.transaction_history.append(penalty)
        else:
            reward = self.calculate_reward(order_value)
            self.transaction_history.append(reward)

        # Keep only last N transactions
        if len(self.transaction_history) > Config.MAX_TRANSACTIONS:
            self.transaction_history.pop(0)

        # Compute weighted score
        raw_score = sum(self.transaction_history)

        # Normalize score between 0 and 10
        self.score = np.clip(((raw_score - Config.MIN_SCORE) / (Config.MAX_SCORE - Config.MIN_SCORE)) * 10, 0, 10)

        return round(self.score, 2)
