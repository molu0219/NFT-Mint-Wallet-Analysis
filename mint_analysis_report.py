# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 15:52:25 2023

@author: Joey Chen
"""


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def print_analysis(tokenName):
    
    
    data_path = "./result/statistic/"+str(tokenName)
    statistic_df = pd.read_pickle(data_path+"/"+str(tokenName)+"_statistic.pkl")
    
    contract_address = statistic_df['contract_address']
    rate = statistic_df['rate'][0]
    total_supply = statistic_df['total_supply'][0]
    address_type_mint_counts = statistic_df['address_type_mint_counts'][0]
    group_type_counts = statistic_df['group_type_counts'][0]
    group_type_mint_counts = statistic_df['group_type_mint_counts'][0]
    group_size_sorted = statistic_df['group_size_sorted'][0]
    group_mint_sorted = statistic_df['group_mint_sorted'][0]
    

    
    print("======== NFT Mint Stage Analysis ======== ")
    print("")
    print("Contract Address: ",contract_address)
    print("TokenName           : ",tokenName)
    print("Participated Rate   : ",rate[0],"%")
    print("Allocation Rate     : ",rate[1],"%")
    print("Greed Rate          : ",rate[2],"%")
    print("")
    print("======== Supply Allocation Analysis ========")
    print("")
    print("Total Supply                                           : ",total_supply)
    print("---- Minted by Independent Wallet                      : ",address_type_mint_counts[0]," (",round(address_type_mint_counts[0]/total_supply*100,2), "%)")
    print("---- Minted by Related Wallet                          : ",address_type_mint_counts[1]," (",round(address_type_mint_counts[1]/total_supply*100,2), "%)")
    print("---- Minted by Independent Bot                         : ",address_type_mint_counts[4]," (",round(address_type_mint_counts[4]/total_supply*100,2), "%)")
    print("---- Minted by Related Bot                             : ",address_type_mint_counts[7]," (",round(address_type_mint_counts[7]/total_supply*100,2), "%)")
    print("")
    print("---- Minted by Team Wallet   (Official)                : ",address_type_mint_counts[3]," (",round(address_type_mint_counts[3]/total_supply*100,2), "%)")
    print("---- Minted by Team Bot      (Official)                : ",address_type_mint_counts[5]," (",round(address_type_mint_counts[5]/total_supply*100,2), "%)") 
    print("---- Minted by Wallet Related to Team                  : ",address_type_mint_counts[2]," (",round(address_type_mint_counts[2]/total_supply*100,2), "%)")
    print("---- Minted by Bot Related to Team                     : ",address_type_mint_counts[6]," (",round(address_type_mint_counts[6]/total_supply*100,2), "%)")
    print("")
    print(" (Team Wallet              : Token Contract Creator by default           ) ")
    print(" (Related Wallet           : Wallets have txn connections                ) ")
    print(" (Related Contract         : Bot by same creators                        ) ")
    print(" (Wallet Related to Team   : Wallets have txn connections to team wallet ) ")
    print(" (Contract Related to Team : Bot Creator related to team wallet          ) ")
    print("")
    print("======== Mint Address Group Analysis ========")
    print("")
    print("Participated Mint Address                              : ",np.sum(group_size_sorted)) 
    print("")
    total = len(group_size_sorted)
    print("Groups                                                 : ",total)
    print("---- Group is Independent Wallet                       : ",group_type_counts[0]," (",round(group_type_counts[0]/total*100,2), "%)")
    print("---- Group is Related Wallet                           : ",group_type_counts[1]," (",round(group_type_counts[1]/total*100,2), "%)")
    print("---- Group is Independent Bot                          : ",group_type_counts[4]," (",round(group_type_counts[4]/total*100,2), "%)")
    print("---- Group is Related Bot                              : ",group_type_counts[7]," (",round(group_type_counts[7]/total*100,2), "%)")
    print("---- Group is Team Wallet   (Official)                 : ",group_type_counts[3]," (",round(group_type_counts[3]/total*100,2), "%)")
    print("---- Group is Team Bot      (Official)                 : ",group_type_counts[5]," (",round(group_type_counts[5]/total*100,2), "%)")
    print("---- Group is Wallet Related to Team                   : ",group_type_counts[2]," (",round(group_type_counts[2]/total*100,2), "%)")
    print("---- Group is Bot Related to Team                      : ",group_type_counts[6]," (",round(group_type_counts[6]/total*100,2), "%)")
    print("")
    print("---- Mint of Group is Independent Wallet               : ",group_type_mint_counts[0]," (",round(group_type_mint_counts[0]/total_supply*100,2), "%)")
    print("---- Mint of Group is Related Wallet                   : ",group_type_mint_counts[1]," (",round(group_type_mint_counts[1]/total_supply*100,2), "%)")
    print("---- Mint of Group is Independent Bot                  : ",group_type_mint_counts[4]," (",round(group_type_mint_counts[4]/total_supply*100,2), "%)")
    print("---- Mint of Group is Related Bot                      : ",group_type_mint_counts[7]," (",round(group_type_mint_counts[7]/total_supply*100,2), "%)")
    print("---- Mint of Group is Team Wallet   (Official)         : ",group_type_mint_counts[3]," (",round(group_type_mint_counts[3]/total_supply*100,2), "%)")
    print("---- Mins of Group is Team Bot      (Official)         : ",group_type_mint_counts[5]," (",round(group_type_mint_counts[5]/total_supply*100,2), "%)")
    print("---- Mint of Group is Wallet Related to Team           : ",group_type_mint_counts[2]," (",round(group_type_mint_counts[2]/total_supply*100,2), "%)")
    print("---- Mint of Group is Bot Related to Team              : ",group_type_mint_counts[6]," (",round(group_type_mint_counts[6]/total_supply*100,2), "%)")
    print("")
    print("Avg Mint per Group                                     : ", round(np.divide(total_supply,total+0.000001),2)," mints" )
    print("---- Avg Mint / Group is Independent Wallet            : ", round(np.divide(group_type_mint_counts[0],group_type_counts[0]+0.000001),2)," mints" )
    print("---- Avg Mint / Group is Related Wallet                : ", round(np.divide(group_type_mint_counts[1],group_type_counts[1]+0.000001),2)," mints" )
    print("---- Avg Mint / Group is Independent Contract(bot)     : ", round(np.divide(group_type_mint_counts[4],group_type_counts[4]+0.000001),2)," mints" )
    print("---- Avg Mint / Group is Related Contract(bot)         : ", round(np.divide(group_type_mint_counts[7],group_type_counts[7]+0.000001),2)," mints" )
    print("---- Avg Mint / Group is Team Wallet   (Official)      : ", round(np.divide(group_type_mint_counts[3],group_type_counts[3]+0.000001),2)," mints" )
    print("---- Avg Mint / Group is Team Bot      (Official)      : ", round(np.divide(group_type_mint_counts[5],group_type_counts[5]+0.000001),2)," mints" )
    print("---- Avg Mint / Group is Wallet Related to Team        : ", round(np.divide(group_type_mint_counts[2],group_type_counts[2]+0.000001),2)," mints" )
    print("---- Avg Mint / Group is Bot Related to Team           : ", round(np.divide(group_type_mint_counts[6],group_type_counts[6]+0.000001),2)," mints" )
    
    print("")
    print("======== Group Rank ========")
    print("")
    print("Top 10 Biggeset Groups : ")
    for i in range(10):
        print("    Top",i+1,"Group has : ",group_size_sorted[i]," wallets or bots")
    
    print("    Top 10 Groups contain",round(np.sum(group_size_sorted[0:10])/np.sum(group_size_sorted)*100,2),"% of participated addresses")
    
    print("")
    print("======== Mint Rank ========")
    print("")
    print("Top 10 mints in Groups : ")
    for i in range(10):
        print("    Top",i+1,": ",group_mint_sorted[i]," (",round(group_mint_sorted[i]/total_supply*100,2),"%) mints")
    
    print("    Top 10 Groups minted",round(np.sum(group_mint_sorted[0:10])/total_supply*100,2),"% of total supply")
    

def plot_analysis(tokenName):
    
    plot_path = "./result/plot/"+str(tokenName)
    
    data_path = "./result/data/"+str(tokenName)
    statistic_path = "./result/statistic/"+str(tokenName)
    
    address_analysis_df = pd.read_pickle(data_path+"/"+str(tokenName)+"_address.pkl")
    group_analysis_df=  pd.read_pickle(data_path+"/"+str(tokenName)+"_group.pkl")
    statistic_df = pd.read_pickle(statistic_path+"/"+str(tokenName)+"_statistic.pkl")

    
    
    address_txn_size = address_analysis_df['Txn_size'].values.tolist()
    address_txn_size =[ x[0] for x in address_txn_size]
    address_type_mint_counts = statistic_df['address_type_mint_counts'][0]
    group_type_counts = statistic_df['group_type_counts'][0]
    group_type_mint_counts = statistic_df['group_type_mint_counts'][0]
    active_rate = statistic_df['active_rate'].values.tolist()[0]
    
    plt.figure(figsize=(9,6))   
    
    labels = ["Independent Wallet","Related Wallet","Wallet Related to Team","Team Wallet (Official)","Independent Bot","Team Bot (Official)","Bot Related to Team","Related Bot"]      # 製作圓餅圖的類別標籤
    
    size =  address_type_mint_counts 
    
    label = [ labels[i] for i in range(len(size)) if size[i] !=0]
    size = [ x for x in size if x!= 0]
    
    pie_label = [""]*len(size)              
    
    plt.pie(size,                           
            labels = pie_label,               
            autopct= '%1.1f%%',            
            shadow=True)                  
    
    plt.axis('equal')                                          
    plt.title("Supply Allocation", {"fontsize" : 18}) 
    plt.legend(loc = 2,labels=label)                                  
    plt.savefig(plot_path+"/"+str(tokenName)+"_Supply_Allocation.png",dpi=300)
    plt.show()
    plt.close()
    
    # Avg Group 
    
    plt.figure(figsize=(10,6))
    
    label = [labels[i] for i in range(len(group_type_mint_counts)) if group_type_mint_counts[i] != 0]
    group_type_mint_counts = [group_type_mint_counts[i] for i in range(len(group_type_mint_counts)) if group_type_mint_counts[i] != 0]
    group_type_counts = [group_type_counts[i] for i in range(len(group_type_counts)) if group_type_counts[i] != 0]
    
    x = np.arange(0, len(group_type_counts), 1)
    
    plt.barh(x - 0.2, group_type_mint_counts, 0.4, label = 'Mints', color='orange', alpha=0.8)
    for a, b in zip(group_type_mint_counts,x):
        if a != 0:
            plt.text(a + 30, b - .2, str(int(a))+" mints", color='orange', ha='center', va= 'bottom',fontsize=10)
            
    plt.barh(x + 0.2, group_type_counts, 0.4, label = 'Wallet/Bot Amount', color='blue', alpha=0.8)
    for a, b in zip(group_type_counts,x):
        if a != 0:
            plt.text(a +30, b + .2, str(int(a))+ " groups ", color='blue', ha='center', va= 'bottom',fontsize=10)
          
    plt.grid(True)
    plt.yticks(x, label)
    plt.ylabel("Group Type")
    plt.xlabel("Mint")
    plt.title("Group's Wallet/bot Amount and Mints Amount")
    plt.legend()
    
    plt.savefig(plot_path+"/"+str(tokenName)+"Group_Type_Mint_Address.png",dpi=300)
    plt.show()
    
    # Rank
    size_sort = group_analysis_df.sort_values(by=["Size"], ascending=False)[0:10]
    mint_sort = group_analysis_df.sort_values(by=["Mint"], ascending=False)[0:10]
    
    
    fig, ax1 = plt.subplots()
    x = np.arange(0, 10, 1)
    ax1.plot(x,size_sort['Mint']) 
    ax1.set_ylabel('Mints')
    ax1.legend(['Mints per Group'], loc="upper left")
    ax2 = ax1.twinx()
    ax2.bar(x, size_sort["Size"], width=0.5, alpha=0.5, color='orange')
    ax2.grid(True) # turn off grid #2
    ax2.set_ylabel('Wallet/Bot Amount')
    ax2.legend(['Wallet/Bot Amount'], loc="upper right")
    plt.xticks(range(10),['Top1', 'Top2', 'Top3', 'Top4', 'Top5', 'Top6', 'Top7', 'Top8', 'Top9', 'Top10'])
    plt.title("Top 10 Biggest Group")
    for a,b in zip(x,size_sort["Size"]):
    
        plt.text(a, b+0.05, '%.0f' % b, ha='center', va= 'bottom',fontsize=10, color='orange')
    
    plt.savefig(plot_path+"/"+str(tokenName)+"_Top10_Size.png",dpi=300)
    plt.show()
    
    fig, ax1 = plt.subplots()
    ax1.plot(x,mint_sort['Size']) 
    ax1.set_ylabel('Wallet/Bot Amount')
    ax1.legend(['Wallet/Bot Amount'], loc="upper left")
    ax2 = ax1.twinx()
    ax2.bar(x, mint_sort["Mint"], width=0.5, alpha=0.5, color='orange')
    ax2.grid(True) # turn off grid #2
    ax2.set_ylabel('Mints per Group')
    ax2.legend(['Mints per Group'], loc="upper right")
    plt.xticks(range(10),['Top1', 'Top2', 'Top3', 'Top4', 'Top5', 'Top6', 'Top7', 'Top8', 'Top9', 'Top10'])
    plt.title("Top 10 Mints by Group")
    for a,b in zip(x,mint_sort["Mint"]):
    
        plt.text(a, b+0.05, '%.0f' % b, ha='center', va= 'bottom',fontsize=10, color='orange')
    
    plt.savefig(plot_path+"/"+str(tokenName)+"_Top10_Mint.png",dpi=300)
    plt.show()
    
    # Active Rate
    
    
    address_txn_size = address_analysis_df['Txn_size'].values.tolist()
    address_txn_size =[ x[0] for x in address_txn_size]
    active_rate = statistic_df['active_rate'].values.tolist()[0]
    
    
    test = sorted(range(len(address_txn_size)), key=lambda k: address_txn_size[k])
    
    # test = sorted(range(len(active_rate)), key=lambda k: active_rate[k])
    
    address_txn_size = [ address_txn_size[x] for x in test]
    active_rate = [ active_rate[x] for x in test]
    
    
    # address_txn_size = sorted(address_txn_size)
    # active_rate = sorted(active_rate)

    x = np.arange(0, len(active_rate), 1)
    
    fig, ax1 = plt.subplots()
    ax1.plot(x,active_rate) 
    ax1.set_ylabel('active rate')
    ax1.legend(['active rate'], loc="upper left")
    ax2 = ax1.twinx()
    ax2.bar(x, address_txn_size, width=0.5, alpha=0.5, color='orange')
    ax2.grid(True) # turn off grid #2
    ax2.set_ylabel('address txn counts')
    ax2.legend(['address txn counts'], loc="upper right")
    plt.title("Active Rate by address")
    
    plt.show()
    
