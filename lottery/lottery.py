import sys
import time
import random

from P2P import P2P
from Block import Block
from BlockChain import BlockChain
from Transaction import Transaction
from MemPool import MemPool
from ConsensusProtocol import ConsensusProtocol


#Block Chain Implementation
n1 = BlockChain()
n2 = BlockChain()
n3 = BlockChain()
n4 = BlockChain()

#Peer to Peer Implementation
Node1 = P2P("127.0.0.1", 8001, "Node1")
Node2 = P2P("127.0.0.1", 8002, "Node2")
Node3 = P2P("127.0.0.1", 8003, "Node3")
Node4 = P2P("127.0.0.1", 8004, "Node4")

#MemPool Implementation
mempool1 = "MEMPOOL1.txt"
mempool2 = "MEMPOOL2.txt"
mempool3 = "MEMPOOL3.txt"
mempool4 = "MEMPOOL4.txt"

n1_mempool = MemPool(mempool1)
n2_mempool = MemPool(mempool2)
n3_mempool = MemPool(mempool3)
n4_mempool = MemPool(mempool4)

nodes_dict = {"Node1":[n1, Node1, n1_mempool], "Node2":[n2, Node2, n2_mempool], "Node3":[n3, Node3, n3_mempool], "Node4":[n4, Node4, n4_mempool]}
size = 2 #The amount of transactions a block can take.


#Initates and starts the nodes.
Node1.start()
Node2.start()
Node3.start()
Node4.start()

time.sleep(1)

#Node connections
print("\n")
Node1.connect_with_node('127.0.0.1', 8002)
Node2.connect_with_node('127.0.0.1', 8001)

Node2.connect_with_node('127.0.0.1', 8003)
Node3.connect_with_node('127.0.0.1', 8002)

Node3.connect_with_node('127.0.0.1', 8004)
Node4.connect_with_node('127.0.0.1', 8003)

Node4.connect_with_node('127.0.0.1', 8001)
Node1.connect_with_node('127.0.0.1', 8004)



blocks = int(input("\nHow many blocks should be mined? "))

#Asks the user/client for additional transactions if wanted. These transactions will then be put in all the MemPools.
print("\nEnter transactions for the MemPool. Make sure to enter in this format: 'from_address' 'to_address' 'amount'")
while True:
    val = input("(Enter 1 to exit) Enter Transaction:")
    
    if(val == "1"):
        break
    else:
        n1_mempool.add_tran(val)
        n2_mempool.add_tran(val)
        n3_mempool.add_tran(val)
        n4_mempool.add_tran(val)


for iter in range(blocks):

    rates = [0, 1, 2, 3]

    rate1 = random.choice(rates)
    rates.remove(rate1)
    rate2 = random.choice(rates)
    rates.remove(rate2)
    rate3 = random.choice(rates)
    rates.remove(rate3)
    rate4 = random.choice(rates)
    rates.remove(rate4)
    
    
    #Arbitrary computational powers for each node. Changes randomly after each newly mined block.
    n1_rate = n1.set_rate(rate1)
    n2_rate = n2.set_rate(rate2)
    n3_rate = n3.set_rate(rate3)
    n4_rate = n4.set_rate(rate4)



    #Arbitrary network speeds for each node. This is useful for the competing chains issue.
    n1_network_speed = n1.set_network_speed(0)
    n2_network_speed = n1.set_network_speed(1)
    n3_network_speed = n1.set_network_speed(2)
    n4_network_speed = n1.set_network_speed(3)
    
    n_dict = nodes_dict

    node_rates = {"Node1":n1_rate, "Node2":n2_rate, "Node3":n3_rate, "Node4":n4_rate}
    fastest_rate = min(node_rates.values())
    fastest_rates = [k for k in node_rates if node_rates[k] == fastest_rate] #List of the fastest rates.

    node_network_speeds = {"Node1":n1_network_speed, "Node2":n2_network_speed, "Node3":n3_network_speed, "Node4":n4_network_speed}
    fastest_speed = min(node_network_speeds.values())
    fastest_speeds = [k for k in node_network_speeds if node_network_speeds[k] == fastest_speed] #List of the fastest network speeds.

    from_address = n1_mempool.from_address
    to_address = n1_mempool.to_address
    amount = n1_mempool.amount



    #Starts the mining process.
    if(len(fastest_rates) == 1):
        print("\n")
        print("Nodes Starting Mining")
        for key, value in n_dict.items():
            if(key == fastest_rates[0]):
                miner = key
                n_miner = value[0]
                n_miner.pending_transactions = []
                n_mempool = value[2]
             

                for i in range(size):
                    n_miner.create_transaction(Transaction(str(from_address[i]), str(to_address[i]), float(amount[i])))
                    data = n_miner.pending_transactions

                print(miner, "Mined Block")
                n_miner.mine_pending_transaction()
                mined_block = n_miner.chain[-1]
                value[1].send_to_nodes(mined_block.block_dict())
                
                time.sleep(1)

        #Consensus Protocol
        c = ConsensusProtocol(mined_block, data)
        c.agree_or_disagree(n_dict, n_miner)
        node_list = c.consensus(miner, n_mempool, n1, n2, n3, n4)

        for key, value in n_dict.items(): #Makes sure that all the MemPools are the same.
            if(miner != key):
                n_mempool.create_replica(value[2].node_mempool)


        n1 = node_list[0]
        n2 = node_list[1]
        n3 = node_list[2]
        n4 = node_list[3]

        n1_mempool = MemPool(mempool1)
        n2_mempool = MemPool(mempool2)
        n3_mempool = MemPool(mempool3)
        n4_mempool = MemPool(mempool4)

    elif(len(fastest_rates) > 1): #Competing Chains Issue.
        print("\n")
        print("Nodes Starting Mining")
        print("COMPETING CHAINS ISSUE\n")

        miners = []
        n_miners = []
        mined_block = []
        data = []
        n_mempool = []

        for x in range(len(fastest_rates)):
            for key, value in n_dict.items():
                if(key == fastest_rates[x]):                    
                    
                    miners.append(key)
                    n_miners.append(value[0])
                    n_miners[x].pending_transactions = []
                    n_mempool.append(value[2])
             

                    for i in range(size):
                        n_miners[x].create_transaction(Transaction(str(from_address[i]), str(to_address[i]), float(amount[i])))
                        data.append(n_miners[x].pending_transactions)

                    print(miners[x], "Mined Block")
                    n_miners[x].mine_pending_transaction()

                    
                    mined_block.append(n_miners[x].chain[-1])
        
        #Consensus Protocol
        for x in range(len(fastest_speeds)):
            for key, value in n_dict.items():
                if(key == fastest_speeds[0]):
                    value[1].send_to_nodes(mined_block[x].block_dict())

                    time.sleep(3)

                    c = ConsensusProtocol(mined_block[x], data[x])
                    c.agree_or_disagree(n_dict, n_miners[x])
                    node_list = c.consensus(miners[x], n_mempool[x], n1, n2, n3, n4)

                    for key, value in n_dict.items(): #Makes sure that all the MemPools are the same
                        if(miners[x] != key):
                            n_mempool[x].create_replica(value[2].node_mempool)


                    n1 = node_list[0]
                    n2 = node_list[1]
                    n3 = node_list[2]
                    n4 = node_list[3]

                    n1_mempool = MemPool(mempool1)
                    n2_mempool = MemPool(mempool2)
                    n3_mempool = MemPool(mempool3)
                    n4_mempool = MemPool(mempool4)
                        
    


n_dict = {"Node1":[n1, Node1, n1_mempool], "Node2":[n2, Node2, n2_mempool], "Node3":[n3, Node3, n3_mempool], "Node4":[n4, Node4, n4_mempool]}

#Prints all chains for all nodes.
for key, value in n_dict.items():
    value[0].print_block_chain(key)