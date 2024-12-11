from flask import Flask, jsonify
from blockchain import Blockchain





app = Flask(__name__)

blockchain = Blockchain()

@app.route('/mine_block', methods=['GET'])
def mine_block():
    """minerando um block!"""

    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {'mensage': 'primeiro block!!',
                'index':block['index'],
                'timespamp':block['timestamp']}