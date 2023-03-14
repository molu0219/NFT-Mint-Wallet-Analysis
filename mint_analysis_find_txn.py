#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 27 13:59:21 2022

@author: bigdatamobile

"""

import json
import pandas as pd
from endpoints.accounts import accounts
from endpoints.contracts import contracts
from endpoints.proxy import proxy
import pickle
import time


# =============================================================================
# end points loading
# =============================================================================



def find_address_txn(index):
    
    
    with open("./config/config.json", newline='') as jsonfile:
        config = json.load(jsonfile)
    with open("./config/config_key.json", newline='') as jsonfile:
        config_key = json.load(jsonfile)
    
    
    address = config['address']
    offset = config['offset']
    page = config['page']
    startblk = config['startblk']
    thread_count = config['thread']
    api_index = index % thread_count
    
    proxy_api = proxy(str(config_key['etherscan_key'+str(api_index)]))
    accounts_api = accounts(str(config_key['etherscan_key'+str(api_index)]))
    contracts_api = contracts(str(config_key['etherscan_key'+str(api_index)]))
    
    accounts_api_backup = accounts(str(config_key['etherscan_key_backup']))
    
    endblk = int(proxy_api.eth_block_num(),base = 16)
    
    address_txn = []
    address_txn_time = []
    address_txn_size = []
    
    with open("./address_txn/sub_address/"+str(index), "rb") as fp:   
        mint_address = pickle.load(fp) 

    address_self_related = []
    
    
    for i in range(len(mint_address)):
        
        time.sleep(0.33)
        
        
        address = mint_address[i]
           
        # Check mint address is wallet or contract
            

        address_status = contracts_api.get_contract_creation(contract_address = address)
     
    
        if int(address_status['status']) == 1:  

            address_self_related.append(["bot",address_status['result'][0]['contractCreator']])
            
            
 
            try:
                address_txn = accounts_api.get_normal_txn_by_address(address = address_status['result'][0]['contractCreator'],
                                                       startblk = startblk,
                                                       endblk = endblk,
                                                       page = page,
                                                       offset =  offset,
                                                       sort='desc')
            except:
                print("API max rate",address)
       
            address_txn_df = pd.DataFrame(address_txn)
            address_txn_time.append(address_txn_df['timeStamp'])
            address_txn_size.append(len(address_txn_df))  


        else:
            
            try:
                address_txn = accounts_api.get_normal_txn_by_address(address = address,
                                                       startblk = startblk,
                                                       endblk = endblk,
                                                       page = page,
                                                       offset =  offset,
                                                       sort='desc')
            except:
                print("API max rate",address)
            
   
            address_txn_df = pd.DataFrame(address_txn)
            
            try:
                address_from = address_txn_df[address_txn_df['to'] == address]['from'].tolist()
            except:
                address_txn = accounts_api_backup.get_normal_txn_by_address(address = address,
                                                       startblk = startblk,
                                                       endblk = endblk,
                                                       page = page,
                                                       offset =  offset,
                                                       sort='desc')
                address_txn_df = pd.DataFrame(address_txn)
                address_from = address_txn_df[address_txn_df['to'] == address]['from'].tolist()
                
            address_to   = address_txn_df[address_txn_df['from'] == address]['to'].tolist()
            address_txn_time.append(address_txn_df['timeStamp'])
            address_txn_size.append(len(address_txn_df))
            address_self_related.append(address_from + address_to)
        
    address_self_related_df = pd.DataFrame(address_self_related)
    address_txn_time_df = pd.DataFrame(address_txn_time)
    address_txn_size_df = pd.DataFrame(address_txn_size)
    address_self_related_df.to_pickle("./address_txn/sub_address_df/"+str(index)+".pkl")
    address_txn_time_df.to_pickle("./address_txn/sub_address_df/"+str(index)+"_time.pkl")
    address_txn_size_df.to_pickle("./address_txn/sub_address_df/"+str(index)+"_size.pkl")
   