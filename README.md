# Blockchain Fundamentals — A Blockchain Built From Scratch in Python

A working blockchain implemented from first principles: block hashing,
proof-of-work mining, chain validation, and tamper detection — no
external blockchain libraries. Every line of the consensus logic here
is mine, which means I can explain any of it in detail, not just
recite that "it uses hashing."

## Why I built this

My Diploma in Business & Financial Technology at NYP covers a
blockchain/fintech module, and it left me wanting to know exactly
*how* the "trustless" part of a blockchain actually works mechanically
— not just the buzzwords. Reading about proof-of-work is one thing;
watching a chain's validation flip from `True` to `False` the instant
a historical value is edited is what actually made it click. This
project is the result of chasing that down until I could rebuild the
core mechanics myself, which felt directly relevant given banks like
JPMorgan run their own blockchain infrastructure (Kinexys, formerly
Onyx) for things like wholesale payments and tokenised assets.

## What it does

- Bundles transactions into `Block`s and chains them via SHA-256 hash
  pointers
- Mines new blocks with adjustable-difficulty proof-of-work
- Validates the full chain's integrity in one call: `is_chain_valid()`
- Computes an address's balance by replaying the transaction history
- Ships with a runnable demo **and** a live tampering demonstration —
  you can watch validation fail in real time

## Project structure

```
blockchain-fundamentals/
├── blockchain/
│   ├── block.py         # Block: hashing + serialisation
│   ├── transaction.py   # Transaction: sender/receiver/amount
│   └── chain.py         # Blockchain: mining + validation
├── tests/
│   └── test_blockchain.py
├── demo.py               # runnable end-to-end walkthrough
├── requirements.txt
└── .github/workflows/tests.yml   # CI: runs the test suite on every push
```

## Getting started

```bash
pip install -r requirements.txt
python demo.py
pytest -v
```

## Sample output (`python demo.py`)

```
Building a difficulty-4 demo chain...

Mined block 1: Block(index=1, hash=00008f2adcf1..., nonce=24107)
Mined block 2: Block(index=2, hash=000024b4a432..., nonce=9142)

Balances after 2 blocks:
  ryan: 65.0
  alice: 20.0
  bob: 15.0

Chain valid? True

--- Tampering with block 1 ---
Chain valid after tampering? False
(the edited amount broke block 1's stored hash, which is recomputed
 and compared during validation -- that mismatch is the whole trick.)
```

Note the nonce values (24107, 9142) — that's proof-of-work happening:
tens of thousands of hash attempts to find a nonce that produces a
hash starting with four zeros, purely by brute force.

## How proof-of-work works here

`Blockchain._mine()` increments a block's `nonce` field and
recomputes its SHA-256 hash on every attempt, stopping only when the
hash starts with `difficulty` leading zero characters. There's no
shortcut for this — SHA-256 is designed so the only way to find a
matching nonce is brute force. That asymmetry (hard to find a valid
nonce, trivial to verify one once found) is the entire security model:
it's what makes it expensive to rewrite history but cheap to check
that history hasn't been rewritten.

## How tamper detection works

`is_chain_valid()` walks the chain and, for every block, (1)
recomputes its hash from its current contents and compares it to the
stored hash, and (2) checks that its `previous_hash` still matches the
actual hash of the block before it. Editing anything in a historical
block — even a single transaction amount — changes that block's
recomputed hash, which no longer matches what's stored, which is
caught instantly. To hide the edit, an attacker would have to re-mine
that block *and every block after it*, which is exactly the work
proof-of-work is designed to make expensive.

## What I'd build next

- **Digital signatures** — sign each transaction with the sender's
  private key (ECDSA, the same scheme Bitcoin uses) so a transaction
  can be cryptographically proven to come from its claimed sender,
  not just claimed in plain text
- **A peer-to-peer layer** — multiple nodes that gossip blocks to each
  other and agree on the longest valid chain when they disagree
- **A REST API / CLI wallet** on top of the core chain, so it's
  interactive rather than script-only

I scoped this project to nail the two mechanics that make a
blockchain "trustless" in the first place — proof-of-work and
tamper-evident chaining — before layering on the networking and
cryptography that a production system would need next.

## Tech stack

Python 3.11+, `hashlib` (standard library only for the core), `pytest`
for the test suite, GitHub Actions for CI.
