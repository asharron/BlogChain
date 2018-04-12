from block import Block
from genesis import create_genesis_block
from new_block import next_block
#Create the blockchain
blockchain = [create_genesis_block()]
previous_block = blockchain[0]

num_of_blocks_to_add = 20

#Add blocks to the chain
for i in range(0, num_of_blocks_to_add):
    block_to_add = next_block(previous_block)
    blockchain.append(block_to_add)
    previous_block = block_to_add

    print("Block #{} has been added to the blockchain!".format(block_to_add.index))
    print("Hash : {}\n".format(block_to_add.hash))
