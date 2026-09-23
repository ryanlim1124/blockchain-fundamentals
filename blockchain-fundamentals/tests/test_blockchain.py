"""
Pytest suite covering the properties a blockchain needs to hold: mining
produces a valid chain, tampering is detected, and balances are
computed correctly from transaction history.

Run with: pytest -v
"""

import pytest

from blockchain.chain import Blockchain
from blockchain.transaction import Transaction


@pytest.fixture
def chain():
    c = Blockchain(difficulty=2)  # low difficulty so tests run fast
    c.add_transaction(Transaction("network", "ryan", 50))
    c.mine_pending_transactions()
    return c


def test_genesis_block_exists():
    c = Blockchain(difficulty=2)
    assert len(c.chain) == 1
    assert c.chain[0].index == 0


def test_mining_adds_a_block(chain):
    assert len(chain.chain) == 2
    assert chain.chain[1].index == 1


def test_mined_block_meets_difficulty(chain):
    assert chain.chain[1].hash.startswith("00")


def test_valid_chain_passes_validation(chain):
    assert chain.is_chain_valid() is True


def test_tampering_is_detected(chain):
    chain.chain[1].transactions[0].amount = 999999
    assert chain.is_chain_valid() is False


def test_broken_link_is_detected(chain):
    chain.add_transaction(Transaction("ryan", "alice", 5))
    chain.mine_pending_transactions()
    chain.chain[1].previous_hash = "tampered"
    assert chain.is_chain_valid() is False


def test_balance_tracks_transactions(chain):
    assert chain.get_balance("ryan") == 50
    assert chain.get_balance("nobody") == 0


def test_negative_amount_rejected():
    with pytest.raises(ValueError):
        Transaction("ryan", "alice", -10)


def test_mining_with_no_pending_transactions_raises():
    c = Blockchain(difficulty=2)
    with pytest.raises(ValueError):
        c.mine_pending_transactions()
