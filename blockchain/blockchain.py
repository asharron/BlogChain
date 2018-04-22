from flask import Flask
from flask import request
from block import Block
import datetime as date
import yaml
import json
from genesis import create_genesis_block

node = Flask(__name__)

#Begining of the blockchain
blockchain = [create_genesis_block()]

#Store transactions
this_nodes_transactions = []

miner_address = "q3nf394hjg-random-miner-address-34nf3i4nflkn3oi"
yaml_file = open('nodes.yaml','r')
peer_nodes = yaml.load(yaml_file)
yaml_file.close()

#Helper function for calculating proof of work
def proof_of_work(last_proof):
    #Variable to find next proof of work
    incrementor = last_proof + 1
    #Keep incrementor until divisible by 9
    # and the previous proof of work
    while not (incrementor % 9 == 0 and incrementor % last_proof == 0):
        incrementor += 1

    return incrementor


@node.route('/txion', methods=['POST'])
def transaction():
    if request.method == 'POST':
        #On each new POST request we extract tranaction data
        new_txion = request.get_json()
        #Add transaction to list
        this_nodes_transactions.append(new_txion)
        #Log to console
        print("New Transaction")
        print("From: {0}".format(new_txion['from']))
        print("To: {0}".format(new_txion['to']))
        print("Amount: {0}".format(new_txion['amount']))

        return "Transaction submission successful\n"

@node.route('/mine', methods=['GET'])
def mine():
    #Get the last proof of work
    last_block = blockchain[-1]
    last_proof = last_block.data['proof-of-work']
    #Calculate the proof of work for this block
    proof = proof_of_work(last_proof)
    #Once we find a valid proof of work
    # We know we can mine a block
    # reward the miner by adding a transaction
    this_nodes_transactions.append(
            {"from": "network", "to": miner_address, "amount":1}
            )
    #Now gather the data needed
    new_block_data = {
            "proof-of-work": proof,
            "transactions": list(this_nodes_transactions)
            }
    new_block_index = last_block.index + 1
    new_block_timestamp = this_timestamp = date.datetime.now()
    last_block_hash = last_block.hash
    #Empty transaction list
    this_nodes_transactions[:] = []

    #Creat the new block
    mined_block = Block(
            new_block_index,
            new_block_timestamp,
            new_block_data,
            last_block_hash
            )
    blockchain.append(mined_block)
    return json.dumps({
        "index": new_block_index,
        "date": str(new_block_timestamp),
        "data": new_block_data,
        "hash": mined_block.hash
        })

@node.route('/blocks', methods=['GET'])
def get_blocks():
    chain_to_send = []
    #Convert blocks to dictionaries to later json
    for block in blockchain:
        block_index = str(block.index)
        block_timestamp = str(block.timestamp)
        block_data = str(block.data)
        block_hash = block.hash
        json_block = {
                "index": block_index,
                "timestamp": block_timestamp,
                "data": block_data,
                "hash": block_hash
                }
        chain_to_send.append(json_block)
    #Send our chain to whomever requested it
    chain_to_send = json.dumps(chain_to_send)
    return chain_to_send

@node.route('/updatenodes', methods=['GET','POST'])
def update_nodes():
    #Check if broadcasting to node
    if request.method == 'POST':
        content = request.get_json() #Get json data from server
        new_node_list = content['nodes'] #Grab the node list from json
        yaml_file = open('nodes.yaml','w') #Write new nodes to file
        yaml_file.write(yaml.dump(new_node_list))
        yaml_file.close()
        return "Updated nodes"
    else:
        return 200

def join_network():
    with open('server.txt','r'):
        serverip = f.readline()
    response = request.post(serverip + '/join')

def find_new_chains():
    #Get blockchains of every other node
    other_chains = []
    for node_url in peer_nodes:
        #Grab chains with GET request
        block = requests.get(node_url + "/blocks").content
        #convert json to dic
        block = json.loads(block)
        #Add to list 
        other_chains.append(block)
    return other_chains

def consensus():
    #Grab chains from the other nodes
    other_chains = find_new_chains()
    longest_chain = blockchain
    for chain in other_chains:
        if len(longest_chain) < len(chain):
            longest_chain = chain
    # If the longest chain wasn't ours,
    # then we set our chain to the longest
    blockchain = longest_chain

node.run(host='0.0.0.0')
join_network()
