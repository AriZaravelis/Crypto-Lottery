import hashlib
import time

class Block:
    def __init__(self, timestamp, transactions_list, prev_hash_val=""):
        self.timestamp = timestamp
        self.nonce = 0
        self.transactions_list = transactions_list
        self.prev_hash_val = prev_hash_val
        self.hash_val = self.calc_hash_val()


    def calc_hash_val(self): #Calculates and returns the hash value.
        i = 0
        data = ""
        for x in self.transactions_list:
            data += str(self.transactions_list[i].from_address) + str(self.transactions_list[i].to_address) + str(self.transactions_list[i].amount)
            i += 1

        everything = str(self.timestamp) + str(self.nonce) + str(data) + str(self.prev_hash_val)
        result = hashlib.sha256(everything.encode()) #Converts the string into bytes to be acceptable by hash function.
        hash_val = result.hexdigest() #Returns the encoded data in hexadecimal format.
        return hash_val


    def mine_block(self,diffic): #Mines the block.
        while(self.hash_val[:diffic] != str("").zfill(diffic)):
            self.nonce += 1
            self.hash_val = self.calc_hash_val()
        print("Block mined", self.hash_val, "\n")


    def print_block(self): #Prints block contents.
        print("Timestamp:",(self.timestamp))
        print("Nonce:",(self.nonce))

        i = 0
        print("Block Data:")
        for x in self.transactions_list:
            print("From:", self.transactions_list[i].from_address, "To:", self.transactions_list[i].to_address, "Amount:", self.transactions_list[i].amount)
            i += 1

        print("Previous Hash Value:",(self.prev_hash_val))
        print("Hash Value:",(self.hash_val))


    def block_dict(self): #Dictionary of the block.
        data = ""
        i = 0
        for x in self.transactions_list:
            data += ("From:" + str(self.transactions_list[i].from_address) + " To:" + str(self.transactions_list[i].to_address) + " Amount:" + str(self.transactions_list[i].amount) + " ")
            i += 1

        b = {"Timestamp":self.timestamp, "Nonce":self.nonce, "Transactions List":data, "Previous Hash Value":self.prev_hash_val, "Hash Value":self.hash_val}
        return b


    def check_hash_val(self, n): #This method is used for the consensus protocol.
        i = 0
        data = ""
        for x in self.transactions_list:
            data += str(self.transactions_list[i].from_address) + str(self.transactions_list[i].to_address) + str(self.transactions_list[i].amount)
            i += 1

        everything = str(self.timestamp) + str(n) + str(data) + str(self.prev_hash_val)
        result = hashlib.sha256(everything.encode())
        hash_val = result.hexdigest()

        return hash_val