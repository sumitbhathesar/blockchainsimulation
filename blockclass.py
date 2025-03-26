import hashlib
import time

class Block:
    def __init__(self, index, transactions, previous_hash):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0  # Used for proof-of-work
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_data = f"{self.index}{self.timestamp}{self.transactions}{self.previous_hash}{self.nonce}"
        return hashlib.sha256(block_data.encode()).hexdigest()

    def mine_block(self, difficulty):
        while self.hash[:difficulty] != "0" * difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()

class Blockchain:
    def __init__(self, difficulty=2):
        self.chain = [self.create_genesis_block()]
        self.difficulty = difficulty

    def create_genesis_block(self):
        return Block(0, "Genesis Block", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, transactions):
        new_block = Block(len(self.chain), transactions, self.get_latest_block().hash)
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True

    def tamper_block(self, index, new_data):
        if index > 0 and index < len(self.chain):
            self.chain[index].transactions = new_data
            self.chain[index].hash = self.chain[index].calculate_hash()


if __name__ == "__main__":
    my_blockchain = Blockchain()

# Create Blockchain
my_blockchain = Blockchain(difficulty=3)

# Add Blocks
my_blockchain.add_block("Sumit pays Rohit 10 Ruppees")
my_blockchain.add_block("Rohit pays Amit 50 Ruppees")
my_blockchain.add_block("Amit pays Sonu  100 Ruppees")
my_blockchain.add_block("Sonu pays Monu 500 Ruppees")

# Print Blockchain
for block in my_blockchain.chain:
    print(f"Block {block.index}:")
    print(f" Transactions: {block.transactions}")
    print(f" Previous Hash: {block.previous_hash}")
    print(f" Current Hash: {block.hash}\n")

# Check Blockchain Validity
print("Is blockchain valid?", my_blockchain.is_chain_valid())

# Tamper with the blockchain
my_blockchain.tamper_block(1, "Sumit pays Rohit 100 Ruppees")
print("\nAfter Tampering:")
print("Is blockchain valid?", my_blockchain.is_chain_valid())
