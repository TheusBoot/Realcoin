import datetime
import hashlib
import json
from flask import Flask, jsonify


#bloco01

class Blockchain:

    def __init__(self):
        self.chain = []
        self.chreate_block(proof=1, previous_hash='0')


    def create_block(self,proof, previous_hash):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash}
        
        self.chain.append(block) # adicionando o bloco na blockchain
        
        return block # retorno do block!
    

    def get_previous_block(self): # retornando o bloco anterior!
        return self.chain[-1]
    

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        
    

        
    
    


