

class Blockchain:

    def __init__(self):

        self.transactions = []
        self.chain = []
        self.nodes = set()


        self.new_block(previous_hash='1', proof=100)

    def new_transaction(self, sender, recipient, amount, sign1, sign2, gen, prime):

        self.current_transactions.append({
            'sender': sender, # Sender Public Key
            'recipient': recipient, # Recepient Public Key
            'amount': amount,
            'sign1': sign1, # Signed by sender with their keys
            'sign2': sign2,
            'gen': gen, # Generator used for their keys
            'prime': prime, # Prime used for their keys
        })

        return self.last_block['index'] + 1
        
    @property
    def last_block(self):
        return self.chain[-1]

    def new_block(self, proof, previous_hash):
  

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # Reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)
        return block

    