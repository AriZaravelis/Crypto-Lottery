class MemPool:
    def __init__(self, node_mempool):
        self.node_mempool = node_mempool
        self.from_address = self.read_mempool()
        self.to_address = self.read_mempool()
        self.amount = self.read_mempool()
        
    def read_mempool(self): #Reads MemPool
        self.from_address = []
        self.to_address = []
        self.amount = []

        with open (self.node_mempool) as file:
            for line in file:
                x = line.split(" ")
                x[-1] = x[-1].strip() #Gets rid of \n at the end of each line from the text file
                self.from_address.append(x[0])
                self.to_address.append(x[1])
                self.amount.append(x[2])
        
        return self.amount


    def remove_tran(self, content): #Removes transaction from MemPool
        with open(self.node_mempool, "r") as f:
            lines = f.readlines()
        with open(self.node_mempool, "w") as f:
            for line in lines:
                if line.strip("\n") != content:
                    f.write(line)


    def add_tran(self, content): #Adds transaction to MemPool
        with open(self.node_mempool, "a") as f:
            f.write("\n" + content)


    def create_replica(self, file1): #Makes sure that all the MemPools are always consistent with one another.
        f = open(file1, "r+") 
        f.seek(0) 
        f.truncate() 
        with open(self.node_mempool,"r") as firstfile, open(file1,"a") as secondfile:
            for line in firstfile:
                secondfile.write(line)