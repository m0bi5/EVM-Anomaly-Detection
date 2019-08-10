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

#Establish connection
azure_url="https://thekoolkids.blockchain.azure.com:3200/xcLrJvLcHS-kfj7Zm5ODJuaE"
connection=Web3(Web3.HTTPProvider(azure_url))
connection.middleware_onion.inject(geth_poa_middleware, layer=0)

#Compile contract
compiled_sol = compile_source_file("a.sol")
contract_id, contract_interface = compiled_sol.popitem()

#Address of deployed contract
address = Web3.toChecksumAddress("0xfb7847f8e9Ab54E397428bC7e4896f3a76929c84")
end_point=connection.eth.contract(address=address,abi=contract_interface['abi'])
print(end_point.functions.getVar().call())
