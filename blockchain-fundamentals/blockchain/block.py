"""
block.py
--------
Defines Block: the fundamental unit of the chain.

Each block bundles a batch of transactions together with metadata that
cryptographically links it to the block before it. That link -- every
block storing the *hash* of its predecessor -- is what makes the
structure a "chain", and it's the reason tampering with old data is so
hard to hide: change one byte anywhere in block #3's data and its hash
changes, which breaks the previous_hash pointer stored in block #4,
which breaks #5, and so on to the end of the chain.
"""

import hashlib
import json
import time
from typing import List

from blockchain.transaction import Transaction


class Block:
    def __init__(
        self,
        index: int,
        transactions: List[Transaction],
        previous_hash: str,
        timestamp: float = None,
        nonce: int = 0,
    ):
        self.index = index
        self.timestamp = timestamp or time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.compute_hash()

    def compute_hash(self) -> str:
        """
        Serialise the block's contents into a deterministic string and
        SHA-256 it. `sort_keys=True` matters: it guarantees the same
        block content always produces the same string (and therefore
        the same hash) no matter what order Python happens to store the
        dict keys in.
        """
        block_dict = {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": [t.to_dict() for t in self.transactions],
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
        }
        block_string = json.dumps(block_dict, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def to_dict(self) -> dict:
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": [t.to_dict() for t in self.transactions],
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "hash": self.hash,
        }

    def __repr__(self):
        return f"Block(index={self.index}, hash={self.hash[:12]}..., nonce={self.nonce})"
