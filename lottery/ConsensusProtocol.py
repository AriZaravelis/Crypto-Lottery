from BlockChain import BlockChain
from Block import Block
from MemPool import MemPool
import random
import math

class ConsensusProtocol:
    def __init__(self, mined_block, data):

        self.mined_block = mined_block
        self.mined_block_dict = self.mined_block.block_dict()
        self.timestamp = self.mined_block_dict["Timestamp"]
        self.nonce = self.mined_block_dict["Nonce"]
        self.data = data
        self.prev_hash = self.mined_block_dict["Previous Hash Value"]



    def agree_or_disagree(self, n_dict, n_miner): #Returns agree_count which is the amount of nodes that agree with the newly mined block.
        self.n_miner = n_miner

        self.agree_count = 0
        self.agreed_nodes = []
        self.disagreed_nodes = []

        for key, value in n_dict.items():
            if((n_miner.chain != value[0].chain) & (n_miner.is_chain_valid() == True)):
                    if(self.mined_block_dict["Previous Hash Value"] == value[0].chain[-1].block_dict()["Hash Value"]):
                        if((Block(self.timestamp,self.data,self.prev_hash).check_hash_val(self.nonce) == self.mined_block_dict["Hash Value"]) & (len(n_miner.chain) - len(value[0].chain) == 1)):
                            print(key, "Agreed")
                            self.agree_count +=1
                            value[0].chain.append(self.mined_block)
                            self.agreed_nodes.append(value[0])
                        else:
                            print(key, "Disagreed")
                            self.disagreed_nodes.append(value[0])
                    else:
                        print(key, "Disagreed")
                        self.disagreed_nodes.append(value[0])

        return self.agree_count



    def consensus(self, miner, n_mempool, n1, n2, n3, n4): #Reaches a consensus

        if(self.agree_count >= 2):
            print("Consensus Agreed")
            self.n_miner.award_miner(miner) #Awards mining reward to the miner.

            #Since a miner mined a new block successfully, the recorded transactions in the newly mined block have to be removed from the mempool
            reward = 0
            for x in self.data:
                reward += x.amount
                content = str(x.from_address) + " " + str(x.to_address) + " " + str(math.trunc(x.amount))
                n_mempool.remove_tran(content)


            #Randomly pick the winner of the lottery and give him the lottery reward.
            winner = (random.choice(self.data)).from_address
            print("The winner is", winner, "The reward is:", reward)

            n1 = self.agreed_nodes[0]
            n2 = self.agreed_nodes[0]
            n3 = self.agreed_nodes[0]
            n4 = self.agreed_nodes[0]

        else:
            print("Consensus Disagreed")
            n1 = self.disagreed_nodes[0]
            n2 = self.disagreed_nodes[0]
            n3 = self.disagreed_nodes[0]
            n4 = self.disagreed_nodes[0]

        return [n1, n2, n3, n4]