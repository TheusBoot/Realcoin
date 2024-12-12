from RealCoin import Blockchain
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
import requests
from urllib.parse import urlparse
from uuid import uuid4
from typing import List, Optional


app = FastAPI()

blockchain = Blockchain()

node_address = str(uuid4()).replace('-','')

class MineBlockResponse(BaseModel):
    message: str
    index: int
    timestamp: str

class ChainResponse(BaseModel):
    chain: list
    length: int

class ValidationResponse(BaseModel):
    message: str

class Transaction(BaseModel):
    sender: str
    receiver: str
    amount: float

# Modelo para validar os dados enviados na requisição
class NodeConnection(BaseModel):
    nodes: Optional[List[str]]



@app.get("/mine_block", response_model=MineBlockResponse)
async def mine_block():
    """
    Minera um bloco.
    """
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    blockchain.add_transaction(sender=node_address, receiver = 'Luiz', amount= 1)
    block = blockchain.create_block(proof, previous_hash)
    return {
        "message": "Primeiro bloco minerado com sucesso!",
        "index": block['index'],
        "timestamp": block['timestamp'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
        'transaction': block['transactions']
    }


@app.get("/get_chain", response_model=ChainResponse)
async def get_chain():
    """
    Retorna toda a blockchain.
    """
    return {
        "chain": blockchain.chain,
        "length": len(blockchain.chain)
    }

@app.get("/is_valid", response_model=ValidationResponse)
async def is_valid():
    """
    Verifica se a blockchain é válida.
    """
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        return {"message": "Tudo certo, blockchain válida!"}
    return {"message": "O blockchain não é válido."}




@app.post('/add_transaction')
async def add_transaction(transaction: Transaction):
    """
    Adiciona uma nova transação à blockchain.
    """
    # Adiciona a transação
    index = blockchain.add_transaction(transaction.sender, transaction.receiver, transaction.amount)
    
    # Retorna uma resposta JSON
    return {
        "message": f"Essa transação será adicionada ao bloco: {index}"
    }

@app.post('/connect_node')
async def connect_node(node_connection: NodeConnection):
    """
    Conectar novos nós à blockchain.
    """
    nodes = node_connection.nodes
    if not nodes:
        raise HTTPException(status_code=400, detail="Nenhum node foi fornecido")
    
    for node in nodes:
        blockchain.add_node(node)
        
    response = {
        "message": "Todos os nós foram conectados com sucesso.",
        "total_nodes": list(blockchain.nodes)
    }
    return response


@app.get('/replace_chain')
def replace_chain():
    is_chain_replaced = blockchain.replace_chain()
    if is_chain_replaced:
        response = {'message': 'os nos tinham cadeias diferentes então foi substituida',
                    'new_chain': blockchain.chain}
    else:
        response = {'message': 'Tudo certo, não houve subtituicao',
                    'actual_chain': blockchain.chain}
        
    return response
        

# Rodar a aplicação:
# Para iniciar o servidor, use o comando:
# uvicorn main:app --host 0.0.0.0 --port 5000 --reload




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