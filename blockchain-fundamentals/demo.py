"""
demo.py
-------
Run this to see the whole thing end to end:
  1. Mine a couple of blocks of transactions
  2. Print balances computed from the chain
  3. Prove the chain validates
  4. Tamper with a historical block and prove validation now FAILS

    python demo.py
"""

from blockchain.chain import Blockchain
from blockchain.transaction import Transaction


def main():
    print("Building a difficulty-4 demo chain...\n")
    chain = Blockchain(difficulty=4)

    chain.add_transaction(Transaction("network", "ryan", 100))
    chain.add_transaction(Transaction("ryan", "alice", 30))
    block1 = chain.mine_pending_transactions()
    print(f"Mined block 1: {block1}")

    chain.add_transaction(Transaction("alice", "bob", 10))
    chain.add_transaction(Transaction("ryan", "bob", 5))
    block2 = chain.mine_pending_transactions()
    print(f"Mined block 2: {block2}\n")

    print("Balances after 2 blocks:")
    for name in ["ryan", "alice", "bob"]:
        print(f"  {name}: {chain.get_balance(name)}")

    print(f"\nChain valid? {chain.is_chain_valid()}")

    print("\n--- Tampering with block 1 ---")
    chain.chain[1].transactions[0].amount = 100_000  # sneaky edit, hash NOT recomputed
    print(f"Chain valid after tampering? {chain.is_chain_valid()}")
    print("(the edited amount broke block 1's stored hash, which is recomputed")
    print(" and compared during validation -- that mismatch is the whole trick.)")


if __name__ == "__main__":
    main()
