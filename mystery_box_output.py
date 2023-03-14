# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 10:22:52 2023

@author: Joey Chen
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import json
import sys
import csv
"""
Mystery Box Output
1. connection lines
2. box size
"""

def mystery_box(tokenName):
    
    
    
    
    return True

if __name__ == '__main__':
    
    # contract_address = sys.argv[1]
    # team_address = sys.argv[2]
    
    with open("./config/config.json", newline='') as jsonfile:
        config = json.load(jsonfile)
        
    contract_address = config['contract_address']
    
    
    # Search Database for contract_address

    tokenName = config['tokenName']
 
    data_path = "./result/data/"+str(tokenName)
    address_df = pd.read_pickle(data_path+"/"+str(tokenName)+"_address.pkl")
    
    data_path = "./result/statistic/"+str(tokenName)
    statistic_df = pd.read_pickle(data_path+"/"+str(tokenName)+"_statistic.pkl")
    
    rate = statistic_df['rate'][0]
    mint_address = address_df['Address']
    mint_wallet_related = address_df['Related']
    mint_wallet_related_idx = address_df['Related_idx']
    
    coordinate1 = []
    coordinate2 = []
    point = []
    # clean mint_wallet_related
    size = len(mint_address)
    for i in range(size):
        temp_coordinate1 = []
        temp_coordinate2 = []
        temp_point = []
        
  
        for j in range(len(mint_wallet_related[i])-1):
            
            temp_coordinate1.append([i,0,mint_wallet_related_idx[i][j]])
            temp_coordinate2.append([0,mint_wallet_related[i][j+1],mint_wallet_related_idx[i][j]])
            temp_point.append([i,mint_wallet_related[i][j+1],mint_wallet_related_idx[i][j]])
        
        coordinate1.append(temp_coordinate1)
        coordinate2.append(temp_coordinate2)
        point.append(temp_point)
    
    with open('./result/mystery_box/coord1.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(coordinate1)
    with open('./result/mystery_box/coord2.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(coordinate2)
    with open('./result/mystery_box/point.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(point)
        

"""
Style

clean, diversity, meaningful
tool? paint, geometry 2D line
 


"""
