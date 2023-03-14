#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 27 13:59:21 2022

@author: Joey Chen

"""
import os
import numpy as np
import json
import pandas as pd
from endpoints.accounts import accounts
from endpoints.proxy import proxy
import mint_analysis_find_txn
import pickle
import threading
import time

import shutil
from mint_analysis_report import print_analysis
from mint_analysis_report import plot_analysis



def mint_analysis():
    
    # =============================================================================
    # Config
    # =============================================================================
    
    with open("./config/config.json", newline='') as jsonfile:
        config = json.load(jsonfile)
    with open("./config/config_key.json", newline='') as jsonfile:
        config_key = json.load(jsonfile)
    proxy_api = proxy(str(config_key['etherscan_key0']))
    accounts_api = accounts(str(config_key['etherscan_key0']))

    erc = config['erc']
    address = config['address']
    contract_address = config['contract_address']
    offset = config['offset']
    page = config['page']
    sort = config['sort']
    startblk = config['startblk']
    thread_count = config['thread']
    thread_unit = config['thread_unit']
    team_address = [x.lower() for x in config['team_address']]
    endblk = int(proxy_api.eth_block_num(),base = 16)
    
    # =============================================================================
    # Find minted txn
    # =============================================================================
    tokenName = ""
        
    if erc == 721:
        mint_txn = accounts_api.get_erc721_transfer_txn_by_address(address = address,
                                                        contract_address = contract_address,
                                                        page = page,
                                                        offset = offset,
                                                        startblk = startblk,
                                                        endblk = endblk,
                                                        sort = sort)
    elif erc == 1155:
        mint_txn = accounts_api.get_erc1155_transfer_txn_by_address(address = address,
                                                        contract_address = contract_address,
                                                        page = page,
                                                        offset = offset,
                                                        startblk = startblk,
                                                        endblk = endblk,
                                                        sort = sort)
    
    
    # DataFrame
    mint_txn_df = pd.DataFrame(mint_txn)
    mint_counts = mint_txn_df['to'].value_counts()
    mint_address = mint_counts.index.tolist()
    tokenName = mint_txn_df["tokenName"][0]
    #endblk = mint_txn[0]['blockNumber']
    # =============================================================================
    # Find address type and relation
    # =============================================================================
     
    # Find the mint wallet related address
    print("Mint wallet txn analysis...")
    count = 0
    sub_count = thread_count*thread_unit # 3*27
    sub_size = int(len(mint_address)/sub_count)
    
    
    try:
        shutil.rmtree("./address_txn/sub_address", ignore_errors=True)
        shutil.rmtree("./address_txn/sub_address_df", ignore_errors=True)
    except:
        print("Folder not exist")
        
    try:
        os.mkdir("./address_txn/sub_address")
        os.mkdir("./address_txn/sub_address_df")

    except:
        print("Dir already exist")
        
    def job(index):
        print("Thread:",index)
        mint_analysis_find_txn.find_address_txn(index)
        
    if sub_size == 0:
        with open("./address_txn/sub_address/0", "wb") as fp:   #Pickling
            pickle.dump(mint_address, fp)
    else:
        for i in range(sub_count):
            
            if i == sub_count-1:
                
                with open("./address_txn/sub_address/"+str(i), "wb") as fp:   #Pickling
                    pickle.dump(mint_address[i*sub_size:], fp)
            else:
                with open("./address_txn/sub_address/"+str(i), "wb") as fp:   #Pickling
                    pickle.dump(mint_address[i*sub_size:(i+1)*sub_size], fp)
    
    threads = []

    if sub_size == 0:
        threads.append( threading.Thread(target = job,args = [0]))
    
    for i in range(sub_count):
        
        temp = threading.Thread(target = job,args = [i])
        threads.append(temp)
    
    for i in range(len(threads)):     
        time.sleep(0.2)
        threads[i].start()
       
    for t in threads:
        t.join()
    
    # =============================================================================
    # Read Data
    # =============================================================================
    print("Read Mint wallet txn analysis...")
    address_self_related = []
    team_address_self_related = []
    address_txn_time = []
    address_txn_size = []
    
    
    
    # Read address reated wallets
    
    if sub_size == 0:
        address_self_related = pd.read_pickle("./address_txn/sub_address_df/0.pkl").values.tolist()
    else:
        
        for i in range(sub_count):
         
            address_self_related += pd.read_pickle("./address_txn/sub_address_df/"+str(i)+".pkl").values.tolist()
    
    
    # Read team related wallets        
    
    for j in range(len(team_address)):
        
        
        team_address_txn = accounts_api.get_normal_txn_by_address(address = team_address[j],
                                                startblk = startblk,
                                                endblk = endblk,
                                                page = page,
                                                offset = offset,
                                                sort='desc')
    
    team_address_txn_df = pd.DataFrame(team_address_txn)
    
    if len(team_address_txn_df) > 0:
        team_address_address_from = team_address_txn_df[team_address_txn_df['to'] == address]['from'].tolist()
        team_address_address_to   = team_address_txn_df[team_address_txn_df['from'] == address]['to'].tolist()
        
        team_address_self_related += (team_address_address_from + team_address_address_to)
    
    # Read address txn timeStamp and Size
    if sub_size == 0:
        address_txn_time =  pd.read_pickle("./address_txn/sub_address_df/0_time.pkl").values.tolist()
    else:
        for i in range(sub_count):
            address_txn_time += pd.read_pickle("./address_txn/sub_address_df/"+str(i)+"_time.pkl").values.tolist()
    
    if sub_count > len(mint_address) :
        address_txn_size =  pd.read_pickle("./address_txn/sub_address_df/0_size.pkl").values.tolist()
    else:
        for i in range(sub_count):
            address_txn_size += pd.read_pickle("./address_txn/sub_address_df/"+str(i)+"_size.pkl").values.tolist()  
    
    
    # =============================================================================
    # Mark Related Wallets
    # =============================================================================
    print("Mint wallet Marking...")
    mint_address_type=np.zeros(len(mint_address))
    mint_address_count= mint_counts.values
    mint_address_creator=[""]*len(mint_address)
    bot_creator = []
    mint_address_txn = np.zeros(len(mint_address))
    
    
    mint_wallet_related = []
    mint_address_related_idx = []

    
    for i in range(len(mint_address)):
        
        print("wallet index: ",i)
        address = mint_address[i]
        
        # Check mint address is wallet or contract
        address_status = str(address_self_related[i][0])
    
        # Address is ralted to itself
        
        temp_mint_wallet_related = []
        temp_index = []
        
        if address_status == "bot":  
            
            # Mark bot contract address
            address_bot_creator = address_self_related[i][1]
            temp_mint_wallet_related.append(i)
            
            mint_address_creator[i] = address_bot_creator
    
            # find how many bots
            if len(bot_creator) == 0:
                temp_mint_wallet_related.append(-1)
                temp_index.append(-1)
                bot_creator.append(address_bot_creator)
                mint_address_type[i] = 4
                
            else:
                for j in range(len(bot_creator)):
    
                    if address_bot_creator == bot_creator[j]:
                        temp_mint_wallet_related.append(-1*(j+1))
                        temp_index.append(-1*(j+1))
                        mint_address_type[i] = 7
                        break
                    elif j == len(bot_creator)-1:
                        temp_mint_wallet_related.append(-1*(j+2))
                        temp_index.append(-1*(j+2))
                        bot_creator.append(address_bot_creator)
                        mint_address_type[i] = 4
     
            
            # if bot is from official Team
            if address_bot_creator in team_address:
                mint_address_type[i] = 5
            
            
            # if bot txn is related official Team address
            bot_creator_txn = accounts_api.get_normal_txn_by_address(address = address_bot_creator,
                                                    startblk = startblk,
                                                    endblk = endblk,
                                                    page = page,
                                                    offset = offset,
                                                    sort='desc')
            
            bot_creator_txn_df = pd.DataFrame(bot_creator_txn)
            
            if len(bot_creator_txn_df) > 0:
                address_from = bot_creator_txn_df[bot_creator_txn_df['to'] == address]['from'].tolist()
                address_to   = bot_creator_txn_df[bot_creator_txn_df['from'] == address]['to'].tolist()
                
                bot_address_self_related = address_from + address_to
            else: 
                bot_address_self_related = []
            
            for j in team_address:
                if j in bot_address_self_related:
                    mint_address_type[i] = 6
                    break
        
        else:
            
            # Address is ralted to itself
            temp_mint_wallet_related.append(i)
            # Address is wallet and official wallet
            
            if  address in team_address:
                mint_address_type[i] = 3
            # Address is related to other wallet
            
            for j in range(len(mint_address)):
                if mint_address[j] in address_self_related[i] and i!=j:
                    temp_mint_wallet_related.append(j)
                    temp_index.append(address_self_related[i].index(mint_address[j]))
                    mint_address_type[j] = 1
          
            # if wallet is related official Team
                    
            if address in team_address_self_related and address not in team_address:
                mint_address_type[i] = 2
                break
                          
        mint_wallet_related.append(temp_mint_wallet_related)
        mint_address_related_idx.append(temp_index)
        
    # =============================================================================
    # Find Related Group
    # =============================================================================
    
    print("Mint wallet Group Finding...")
    
    t = 3
    p = 0.02
     
    total = 0
    for i in range(t):
        
        total += 333*p*(i+1)

    print("t: ",t*333,"total: ",total,"cost: ",p*t)
            
    
    check_sum = len(mint_address)+1
    check_mint_wallet_related = list(mint_wallet_related)
    
    while check_sum > len(mint_address):
        mint_wallet_group = []
        for i in range(len(check_mint_wallet_related)):
            if len(mint_wallet_group) == 0:
                mint_wallet_group.append(check_mint_wallet_related[i])
            else:
                for j in range(len(mint_wallet_group)):
                    
                    # find all cadidate during search
                    candidate = [ k for k in check_mint_wallet_related[i] if k in mint_wallet_group[j]]  
                    candidate2 = [ k for k in check_mint_wallet_related[i] if k not in mint_wallet_group[j]] 
                    
                    if len(candidate)>0 and j!=i:
                        mint_wallet_group[j] = sorted(mint_wallet_group[j] + candidate2)
                        break
                    elif j == len(mint_wallet_group)-1:
                        mint_wallet_group.append(check_mint_wallet_related[i])
                        
        check_mint_wallet_related = list(mint_wallet_group)
        
        # Check no duplicated wallet in different group
        check = np.zeros(len(mint_address))
        for i in range(len(mint_wallet_group)):
            for j in mint_wallet_group[i]:
                if j>=0:
                    check[j] = check[j] + 1
        check_sum = np.sum(check)
        
    # =============================================================================
    # Behavior Detection (Similar Activity)
    # =============================================================================
    """
    1. From
    2. To 
    3. Time
    4. Similar Txn / total txn
    """
    
    # =============================================================================
    # Analysis
    # =============================================================================
    
    
    print("Statistic analysis...")
    
    plot_path = "./result/plot/"+str(tokenName)
    data_path = "./result/data/"+str(tokenName)
    statistic_path = "./result/statistic/"+str(tokenName)
    
    try:
        shutil.rmtree(plot_path, ignore_errors=True)
        shutil.rmtree(data_path, ignore_errors=True)
        shutil.rmtree(statistic_path, ignore_errors=True)
    except:
        print("Folder not exist")
    
    
    try:
        os.mkdir(plot_path)
        os.mkdir(data_path)
        os.mkdir(statistic_path)
    except:
        print("Dir already exist")
    
    # Mint Address Analysis
    
    dic ={ 
          "Address": mint_address,
          "Type": mint_address_type,
     "Count":mint_address_count,
     "Creator":mint_address_creator,
     "Related":mint_wallet_related,
     "Related_idx": mint_address_related_idx,
     "Count_txn":mint_address_txn,
     "Txn_size": address_txn_size,
     "Txn_time": address_txn_time
    
     }
    
    address_analysis_df = pd.DataFrame(dic)
    address_type_mint_counts = []
    
    for i in range(8):
        address_type_mint_counts.append(address_analysis_df[address_analysis_df['Type'] == i].sum(axis=0))
    
    address_type_mint_counts = [ x.Count for x in address_type_mint_counts]
    
    # Group Analysis
    
    group_size = []
    group_mint = []
    group_type = []
    
    """
        This is the identity 
    """
    
    for i in range(len(mint_wallet_group)):
        count = 0
        temp_test_group = []
        # cumulate amount
        for j in mint_wallet_group[i]:
            
            if j >= 0:
                count = count + mint_counts[j]
                temp_test_group.append(mint_address_type[j])
        group_type.append(temp_test_group)
        group_mint.append(count)
        group_size.append(len(mint_wallet_group[i]))
        
    for i in range(len(group_type)):
        if group_type[i][-1] == 3 and group_type[i][0] !=3:
            group_type[i] = 2
        else:
            group_type[i] = group_type[i][-1]
  
    
    dic ={ "Address": mint_wallet_group,
          "Type": group_type,
     "Mint":group_mint,
     "Size":group_size,
     }
    
    group_analysis_df = pd.DataFrame(dic)
    

    group_size_sorted = sorted(group_size, reverse=True)
    group_mint_sorted = sorted(group_mint, reverse=True)
    
    group_type_counts = np.zeros(8)
    group_type_mint_counts = np.zeros(8)
    
    for i in range(len(group_type)):
        group_type_counts[int(group_type[i])] = group_type_counts[int(group_type[i])] + 1
        group_type_mint_counts[int(group_type[i])] = group_type_mint_counts[int(group_type[i])] + group_mint[i]
        
    
    # =============================================================================
    # Index Rate
    # =============================================================================
    
    
    avg_mint_by_group =len(mint_txn)/len(group_size)
    above_count = 0
    
    for i in range(len(group_size)):  
        temp = group_mint[i]-avg_mint_by_group
        if temp >= 0.0:
            above_count += 1
    
    allocation_rate = np.round(above_count/len(group_size)*100,2)
    participated_rate = np.round(len(mint_counts)/len(mint_txn)*100,2)
    greed_rate = np.round( (1-len(mint_wallet_group)/len(mint_counts))*100,2)
    
    # address active 
    active_rate = []
    address_dur = []
    
    for i in range(len(mint_address)):
        temp = list(address_txn_time[i])
        temp = [x for x in temp if pd.isnull(x) == False]
        dur = abs(int(temp[0])-int(temp[-1])+0.00001)
        address_dur.append(dur)
        active_rate.append(np.round(address_txn_size[i][0]/dur*86400,3)) #avg per day 60*60*24 = 86400

    
    # =============================================================================
    # Statistic Output
    # =============================================================================
    
    dic = {
           "token_name": [tokenName],
           "contract_address": [contract_address],
           "rate":[[participated_rate,allocation_rate,greed_rate]],
           "total_supply": [len(mint_txn)],
           "address_type_mint_counts": [address_type_mint_counts],
           "group_type_counts":[ group_type_counts],
           "group_type_mint_counts": [group_type_mint_counts],
           "group_size_sorted": [group_size_sorted],
           "group_mint_sorted": [group_mint_sorted],  
           "active_rate": [active_rate],
           "address_dur": [address_dur]
           }
    statistic_analysis_df = pd.DataFrame(dic)
    
    address_df_path = (data_path+"/"+str(tokenName)+"_address.pkl")  
    group_df_path = (data_path+"/"+str(tokenName)+"_group.pkl")  
    statistic_analysis_df_path = (statistic_path+"/"+str(tokenName)+"_statistic.pkl")  
    
    address_analysis_df.to_pickle(address_df_path)  
    group_analysis_df.to_pickle(group_df_path)  
    statistic_analysis_df.to_pickle(statistic_analysis_df_path)
    
    return tokenName


if __name__ =="__main__":
    tokenName = mint_analysis()
    print_analysis(tokenName)
    plot_analysis(tokenName)