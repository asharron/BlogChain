import datetime as date
from block import Block

def create_genesis_block():
    #Create beginning block with random value
    return Block(0, date.datetime.now(), {'blog-title':'Gensis Block','blog-content':'This is the genesis block','proof-of-work':9,'transactions':0}, "0")
