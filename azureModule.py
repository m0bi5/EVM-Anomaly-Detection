from web3 import Web3
from web3.middleware import geth_poa_middleware
import os,json,solc

class talkToAzure():
    azure_url="https://thekoolkids.blockchain.azure.com:3200/xcLrJvLcHS-kfj7Zm5ODJuaE"
    connection=Web3(Web3.HTTPProvider(azure_url))
    connection.middleware_onion.inject(geth_poa_middleware, layer=0)
    compiledContract=None
    contractId=None
    contractInterface=None
    contractAddress=None
    contractInfo='latestContractDeployment.txt'
    contract=None

    #Compile solidity code
    def compileSource(self,filePath):
        source=""
        with open(filePath, 'r') as f:
            source = f.read()
        return solc.compile_source(source)

    #Get ready for contract deployment
    def deploymentInit(self,filePath):
        self.compiledContract=self.compileSource(filePath)
        self.contractId,self.contractInterface=self.compiledContract.popitem()
        self.compiledContract=self.contractInterface['abi']
    
    #Get ready to make transactions to contract
    def transactionInit(self):
        data=None
        with open(self.contractInfo,'r') as f:
            data=json.load(f)
        self.compiledContract=data['abi']
        self.contractAddress=data['address']
        self.contract=self.connection.eth.contract(address=self.contractAddress,abi=self.compiledContract)

    #Creates new account for every transaction, !!change this!!
    def makeTransaction(self,sendTo):
        account=self.connection.eth.account.create("SDADASDASDASDADADDAS")
        txn = sendTo.buildTransaction()
        txn['nonce']=self.connection.eth.getTransactionCount(account.address)
        signed = self.connection.eth.account.signTransaction(txn,account.privateKey)
        txnHash = self.connection.eth.sendRawTransaction(signed.rawTransaction)
        txnReceipt = self.connection.eth.waitForTransactionReceipt(txnHash)
        return txnReceipt

    #Deploy contract to azure 
    def deployContract(self):
        contract = self.connection.eth.contract(abi=self.contractInterface['abi'],bytecode=self.contractInterface['bin'])
        txnReceipt = self.makeTransaction(contract.constructor())
        self.contractAddress=txnReceipt['contractAddress']
        write={'address':self.contractAddress,'abi':self.compiledContract}
        print("Successfully deployed {0} to: {1}\n".format(self.contractId, self.contractAddress))
        with open(self.contractInfo,'w') as f:
            json.dump(write,f)

#deploymentObject=talkToAzure()
#deploymentObject.deploymentInit('voteContract.sol')
#deploymentObject.deployContract()
'''
transactionObject=talkToAzure()
transactionObject.transactionInit()
print(transactionObject.contract.functions.get_candidates(0).call())
print(transactionObject.makeTransaction(transactionObject.contract.functions.cast_vote(0)))
print(transactionObject.contract.functions.get_candidates(0).call())


'''