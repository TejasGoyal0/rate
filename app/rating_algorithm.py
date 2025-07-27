import numpy as np
import time
from app.config import Config

class StableReputation:
    def __init__(self):
        self.score = 5.0  # Starting point on 0–10 scale
        self.transaction_history = []  # (delta_score, timestamp)

    def calculate_penalty(self, order_value):
        """Log-scaled penalty for returned orders."""
        scaled = np.log1p(order_value)  # Prevents log(0)
        return -1 * Config.BASE_PENALTY * (1 + Config.VALUE_FACTOR * scaled)

    def calculate_reward(self, order_value):
        """Reward for successful (non-returned) orders."""
        scaled = np.log1p(order_value)
        return Config.BASE_REWARD + (Config.VALUE_FACTOR * scaled)

    def update_score(self, order_value, returned):
        """Update reputation score based on order outcome."""
        delta = self.calculate_penalty(order_value) if returned else self.calculate_reward(order_value)
        self.transaction_history.append((delta, time.time()))

        # Keep history length manageable
        if len(self.transaction_history) > Config.MAX_TRANSACTIONS:
            self.transaction_history.pop(0)

        # Weight recent transactions more
        weights = np.linspace(0.5, 1.0, len(self.transaction_history))
        deltas = np.array([entry[0] for entry in self.transaction_history])
        weighted_sum = np.dot(deltas, weights)

        # Normalize to 0–10 range
        raw_score = weighted_sum
        normalized = ((raw_score - Config.MIN_SCORE) / (Config.MAX_SCORE - Config.MIN_SCORE)) * 10
        self.score = float(np.clip(normalized, 0, 10))

        return round(self.score, 2)
