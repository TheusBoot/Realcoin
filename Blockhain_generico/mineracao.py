from blockchain import Blockchain
from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()

blockchain = Blockchain()

class MineBlockResponse(BaseModel):
    message: str
    index: int
    timestamp: str

class ChainResponse(BaseModel):
    chain: list
    length: int

class ValidationResponse(BaseModel):
    message: str

@app.get("/mine_block", response_model=MineBlockResponse)
async def mine_block():
    """
    Minera um bloco.
    """
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    return {
        "message": "Primeiro bloco minerado com sucesso!",
        "index": block['index'],
        "timestamp": block['timestamp']
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