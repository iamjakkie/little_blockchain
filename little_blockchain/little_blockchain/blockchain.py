import json
import random
import sys 

from datetime import datetime
from hashlib import sha256

sys.setrecursionlimit(50000)

class Blockchain(object):
    def __init__(self) -> None:
        self.chain = []
        self.pending_transactions = []

        print("genesis block")
        self.new_block()

    def new_block(self):
        block = {
            'index': len(self.chain),
            'timestamp': datetime.utcnow().isoformat(),
            'transactions': self.pending_transactions,
            'previous_hash': self.last_block(),
            'nonce': format(random.getrandbits(64), 'x'),
        }

        block_hash = self.hash(block)
        block['hash'] = block_hash

        self.pending_transactions = []
        self.chain.append(block)

        # print(f"created block {block['index']}")
        return block

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return sha256(block_string).hexdigest()

    def last_block(self):
        return self.chain[-1] if self.chain else None

    def new_transaction(self, sender, recipient, amt):
        self.pending_transactions.append({
            'recipient': recipient,
            'sender': sender,
            'amount': amt,
        })

    def proof_of_work(self):
        while True:
            new_block = self.new_block()
            if self.valid_block(new_block):
                break
        
        self.chain.append(new_block)
        print('found a new block: ', new_block)

    @staticmethod
    def valid_block(block):
        return block['hash'].startswith('0000')