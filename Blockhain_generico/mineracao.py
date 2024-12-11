from flask import Flask, jsonify
from blockchain import Blockchain





app = Flask(__name__)

#app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

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
    return jsonify(response), 200


@app.route('/get_chain', methods= ['GET'])
def get_chain():
    """retornar toda blockchain"""
    response = {'chain':blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200


@app.route('/is_valid',methods=['GET'])
def is_valid():
    """Verificando se a blockchain é valida!"""

    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message': 'tudo certo, bloco valido!'}
    else:
        response = {'message': 'o blockchain não é valido'}

    return jsonify(response), 200





app.run(host='0.0.0.0', port=5000)



""" Minerando um bloco!
{
    "index": 5,
    "mensage": "primeiro block!!",
    "timespamp": "2024-12-11 05:08:40.392342"
}
"""



""" RESULTADO DE TODA BLOCKCHAIN!
{
    "chain": [
        {
            "index": 1,
            "previous_hash": "0",
            "proof": 1,
            "timestamp": "2024-12-11 05:06:03.903932"
        },
        {
            "index": 2,
            "previous_hash": "6bd814f358f3563f856254a471b642319c8fa2b546371208ff9b1c2c5e442492",
            "proof": 533,
            "timestamp": "2024-12-11 05:06:28.244192"
        },
        {
            "index": 3,
            "previous_hash": "8e36fe9df16a780c02f5687ea2d2a8707140bf59dc76d3bb369efd3115937982",
            "proof": 45293,
            "timestamp": "2024-12-11 05:06:32.481120"
        },
        {
            "index": 4,
            "previous_hash": "689b48384a386bd8edfceab414c550a55802b6bf8cb6fea0dad24d2ea70b307b",
            "proof": 21391,
            "timestamp": "2024-12-11 05:06:35.738205"
        }
    ],
    "length": 4
}"""