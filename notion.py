# -*- coding: utf-8 -*-
"""
Created on Wed Mar  8 17:18:29 2023

@author: Joey Chen
"""

import os
from notion_client import Client
from pprint import pprint
import requests

# Set up Notion API client
notion = Client(auth="secret_rRbwq2XH9vu2kHwyTMABy84gvGLXBxY2xxNZI6PLXtx")


token = "secret_rRbwq2XH9vu2kHwyTMABy84gvGLXBxY2xxNZI6PLXtx" 
database_id = "079e06017f094cee87e207b2e3fb57b9"
page_id = "d0a87151ad17455398fb866242882958"
block_id = "dccade80716747e3813b30f5e29d217a"

# https://api.notion.com/v1/blocks/{block_id}
# https://api.notion.com/v1/blocks/{block_id}/children
# https://api.notion.com/v1/databases/{}
# https://api.notion.com/v1/pages/{page_id}
# https://api.notion.com/v1/pages/{page_id}/properties/{property_id}

r = requests.get(
    url=" https://api.notion.com/v1/blocks/{}/children".format(block_id) ,
    headers={"Authorization": "Bearer " + token, "Notion-Version": "2021-05-13"},
)
print(r.text)
"""
# Create a new page with the specified properties
new_page = notion.pages.create(
    parent={"database_id": "079e06017f094cee87e207b2e3fb57b9"},
    properties= {
           "Analysis by": {
              
                "type": "select",
                "select": {
             
                    "name": "molu219.NFT",
                    "color": "blue"
                }
            },
            "Last edited time": {
               "date":{"start":"2023"}
            },
            "Greed Rate": {
             
                "type": "number",
                "number": 0.4802
            },
            "Participated Rate": {
                
                "type": "number",
                "number": 0.5626
            },
            "Allocation Rate": {
               
                "type": "number",
                "number": 0.0473
            },
            "Type": {
                "type": "multi_select",
                "multi_select": [{
                    "id": "68eb781c-2833-4858-9fea-32999c8f74c2",
                    "name": "pfp",
                    "color": "default"
                }]
            },
            "Project": {
                "id": "title",
                "type": "title",
                "title": [{
                    "type": "text",
                    "text": {
                        "content": "Whiko",
   
                    },
                    "plain_text": "Whiko",
    
                }]
            }
        }
        
)
"""
