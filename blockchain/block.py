import hashlib as hasher

class Block:

    #Constructor for creating the block 
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.hash_block()

    #Method to hash the block along with its contents
    def hash_block(self):
        sha = hasher.sha256()
        sha.update((str(self.index) +
                str(self.timestamp) +
                str(self.data) + 
                str(self.previous_hash)).encode())

        return sha.hexdigest()
