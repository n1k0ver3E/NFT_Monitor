import json, time, requests
from web3 import Web3
from web3.auto import w3
from web3.middleware import local_filter_middleware
from threading import Thread

import sys, os.path
sys.path.append(os.path.abspath('../'))

from config import params

COLLECTION_CONTRACT_ADDRESS = params['COLLECTION_CONTRACT_ADDRESS']
CONTRACT_ADDRESS= params['CONTRACT_ADDRESS']

bsc = "https://bsc-dataseed1.defibit.io/"
web3 = Web3(Web3.HTTPProvider(bsc))
 
def initEvent():
    contract_ = Web3.toChecksumAddress(CONTRACT_ADDRESS)
    event_filter_ = web3.eth.filter({"address": contract_})
    return event_filter_
    
def returnTransaction(Txn_hash):
    result = dict()
    res = web3.eth.get_transaction(Txn_hash)
    if len(res['input']) == 138: # Only create and modify method have 3 topics
        print("Method does not meet the requirements. ")
        return False
    else:
        topic_0 = res['input'][34:74]
        topic_1 = res['input'][74:74+64]
        topic_2 = res['input'][138:]
        contract_address_ = Web3.toHex(hexstr=topic_0)
        tokenId = Web3.toInt(hexstr=topic_1) 
        
        price_ = Web3.toInt(hexstr=topic_2)
        price = Web3.fromWei(price_,'ether')
        if contract_address_ == COLLECTION_CONTRACT_ADDRESS:    
            result['contract_address'] = contract_address_
            result['tokenId'] = str(tokenId)
            result['price'] = price
            return result
        else:
            print("NFT Contract Address does not Meet Requirement.")
            return False
    
def returnHash(events_filter):
    res = list()
    events = events_filter.get_new_entries()
    if events:
        for event in events:
            if Web3.toHex(event['transactionHash']) not in res:
                res.append(Web3.toHex(event['transactionHash']))
    else:
        return False
        
    return res

# 聪明钱追踪

# 新合约追踪




