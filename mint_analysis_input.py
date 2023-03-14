# -*- coding: utf-8 -*-
"""
Created on Mon Jan  9 20:22:09 2023

@author: Joey Chen
"""

import json
from mint_analysis import mint_analysis
from mint_analysis_report import print_analysis
from mint_analysis_report import plot_analysis
import sys



if __name__ == '__main__':
    
    # contract_address = sys.argv[1]
    # team_address = sys.argv[2]
    
    with open("./config/config.json", newline='') as jsonfile:
        config = json.load(jsonfile)
        
    contract_address = config['contract_address']
    
    
    # Search Database for contract_address
    find = True
    
    if find:
        
        tokenName = config['tokenName']
        try:
            print_analysis(tokenName)
            plot_analysis(tokenName)
        except:
            print("No token Find")
        
    
    else:
        
        tokenName = mint_analysis()
    
        try:
            print_analysis(tokenName)
            plot_analysis(tokenName)
        except:
            print("No token Find")