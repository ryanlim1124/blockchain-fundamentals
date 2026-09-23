"""
chain.py
--------
Blockchain: the ordered list of Blocks, a pool of pending transactions
waiting to be mined, and the two operations that give a blockchain its
guarantees:

1. Proof-of-work mining -- makes ADDING a block expensive.
2. Chain validation      -- makes TAMPERING WITH a block detectable.

Together, those two properties are what let a network of people who
don't trust each other agree on one shared history.
"""

from typing import List

from blockchain.block import Block
from blockchain.transaction import Transaction


class Blockchain:
    def __init__(self, difficulty: int = 4):
        """
        difficulty: how many leading zero-characters a mined block's
        hash must have. Each extra digit multiplies the expected mining
        work by roughly 16x (hex), which is the same lever Bitcoin uses
        to keep block time roughly constant as more miners join.
        """
        self.chain: List[Block] = []
        self.pending_transactions: List[Transaction] = []
        self.difficulty = difficulty
        self._create_genesis_block()

    def _create_genesis_block(self):
        genesis = Block(index=0, transactions=[], previous_hash="0")
        genesis.hash = self._mine(genesis)
        self.chain.append(genesis)

    @property
    def last_block(self) -> Block:
        return self.chain[-1]

    def add_transaction(self, transaction: Transaction):
        self.pending_transactions.append(transaction)

    def _mine(self, block: Block) -> str:
        """
        Proof-of-work: keep incrementing the block's nonce until its
        hash starts with `difficulty` zeros. There is no shortcut --
        SHA-256 is designed so the only way to find such a nonce is
        brute force. That's what makes rewriting history expensive: an
        attacker would have to redo this search for the tampered block
        AND every block mined after it, faster than the honest network
        can extend the real chain.
        """
        block.nonce = 0
        computed_hash = block.compute_hash()
        target = "0" * self.difficulty
        while not computed_hash.startswith(target):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash

    def mine_pending_transactions(self) -> Block:
        if not self.pending_transactions:
            raise ValueError("No pending transactions to mine")

        new_block = Block(
            index=self.last_block.index + 1,
            transactions=self.pending_transactions,
            previous_hash=self.last_block.hash,
        )
        new_block.hash = self._mine(new_block)
        self.chain.append(new_block)
        self.pending_transactions = []
        return new_block

    def is_chain_valid(self) -> bool:
        """
        Walk the chain checking, for every block after the genesis
        block:
          1. Its stored hash still matches a fresh recomputation, i.e.
             nobody edited its transactions/nonce/timestamp after the
             fact.
          2. Its previous_hash still matches the actual hash of the
             block before it, i.e. no block has been swapped out.
          3. It still meets the proof-of-work difficulty target.
        Any one of these failing means the chain has been tampered
        with.
        """
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            if current.hash != current.compute_hash():
                return False
            if current.previous_hash != previous.hash:
                return False
            if not current.hash.startswith("0" * self.difficulty):
                return False

        return True

    def get_balance(self, address: str) -> float:
        """Naive balance: replay every transaction in the chain so far."""
        balance = 0.0
        for block in self.chain:
            for tx in block.transactions:
                if tx.receiver == address:
                    balance += tx.amount
                if tx.sender == address:
                    balance -= tx.amount
        return balance
