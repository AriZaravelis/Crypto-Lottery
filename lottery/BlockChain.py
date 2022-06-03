import hashlib
import time

from Block import Block
from Transaction import Transaction

class BlockChain:
    def __init__(self):
        self.chain = [self.generate_genesis_block(),] #List/Chain of blocks. First block is genesis block.
        self.pending_transactions = []
        self.mining_reward = 100 #Reward for mining a block
        self.diffic = 2 #Establishes difficulty level.


    def generate_genesis_block(self): #Generates the genesis block.
        return Block(time.strftime('%H:%M:%S'),[Transaction(None,None,0),])


    def get_last_block(self):
        return self.chain[-1] #Accessing the last block in a chain


    def mine_pending_transaction(self): #Mines a block and attaches it to the chain.
        self.prev_hash_val = self.get_last_block().hash_val
        block = Block(time.strftime('%H:%M:%S'), self.pending_transactions, self.prev_hash_val)
        block.mine_block(self.diffic)
        self.chain.append(block)
        
    
    def award_miner(self, mining_reward_address): #Awards the miner with the mining reward we specified.
        print(mining_reward_address, "got reward", self.mining_reward)
        self.pending_transactions = [Transaction(None, mining_reward_address, self.mining_reward)] #The system gives the mining reward to the miner


    def create_transaction(self, Transaction):
       self.pending_transactions.append(Transaction)
       

    def get_balance(self, address):
        balance = 0
        for b in self.chain:
            for t in b.transactions_list:
                if t.to_address == address:
                    balance += t.amount
                elif t.from_address == address:
                    balance -= t. amount
        return balance


    def set_rate(self, rate): #Represents the computational power of a node.
        self.rate = rate
        return self.rate


    def set_network_speed(self, speed): #Represents the network speed of a node.
        self.speed = speed
        return self.speed


    def is_chain_valid(self): #Checks if chain and last block are valid.
        for i in range(1, len(self.chain)):
            prevb = self.chain[i-1]
            currb = self.chain[i]
            if(currb.hash_val != currb.calc_hash_val()):
                print("Invalid Block")
                return False
            if(currb.prev_hash_val != prevb.hash_val):
                print("Invalid Chain")
                return False
        return True


    def print_block_chain(self,node): #Prints Block Chain.
        print("\n")
        print(node, "Block Chain:")
        i = 1
        for x in self.chain:
            print("\nBlock #",(i))
            i += 1
            x.print_block()