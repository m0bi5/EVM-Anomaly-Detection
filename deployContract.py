from web3 import Web3
from web3.middleware import geth_poa_middleware
import os
from solc import compile_source

#Solidity compiler
def compile_source_file(file_path):
    source=""
    with open(file_path, 'r') as f:
        source = f.read()
    return compile_source(source)

#Deploy contract to azure 
def deploy_contract(w3, contract_interface):
    contract = w3.eth.contract(
        abi=contract_interface['abi'],
        bytecode=contract_interface['bin'])
    new_account=w3.eth.account.create("SDADASDASDASDADADDAS")
    txn = contract.constructor().buildTransaction()
    txn['nonce']=w3.eth.getTransactionCount(new_account.address)
    print(txn)
    signed = w3.eth.account.signTransaction(txn, new_account.privateKey)
    txn_hash = w3.eth.sendRawTransaction(signed.rawTransaction)  
    txn_receipt = w3.eth.waitForTransactionReceipt(txn_hash)
    print(txn_receipt)
    return txn_receipt['contractAddress']

#Establish connection
azure_url="https://thekoolkids.blockchain.azure.com:3200/xcLrJvLcHS-kfj7Zm5ODJuaE"
connection=Web3(Web3.HTTPProvider(azure_url))
connection.middleware_onion.inject(geth_poa_middleware, layer=0)

compiled_sol = compile_source_file("a.sol")

contract_id, contract_interface = compiled_sol.popitem()

address = deploy_contract(connection, contract_interface)
print("Deployed {0} to: {1}\n".format(contract_id, address))

end_point=connection.eth.contract(address=address,abi=contract_interface['abi'])
print(end_point.functions.getVar().call())
