"""
transaction.py
---------------
A minimal Transaction: who sent what to whom.

Real blockchains (Bitcoin, Ethereum, and JPMorgan's own Kinexys/Onyx
blockchain unit) attach a cryptographic signature here to prove the
sender actually authorised the transfer. This project keeps
transactions unsigned so the code stays focused on the two mechanics
that make a "chain" trustworthy: proof-of-work and hash-linking (see
chain.py). Adding real signatures is the natural next step -- it's
called out in the README under "What I'd build next".
"""

import time


class Transaction:
    """A single transfer of `amount` from `sender` to `receiver`."""

    def __init__(self, sender: str, receiver: str, amount: float, timestamp: float = None):
        if amount <= 0:
            raise ValueError("Transaction amount must be positive")
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.timestamp = timestamp or time.time()

    def to_dict(self) -> dict:
        return {
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": self.amount,
            "timestamp": self.timestamp,
        }

    def __repr__(self):
        return f"Transaction({self.sender} -> {self.receiver}: {self.amount})"
