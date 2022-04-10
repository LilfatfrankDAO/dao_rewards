from flask_restful import Resource
from tracemalloc import start
import requests
import json
import pandas as pd
import time

import os
etherscan_api = os.getenv('etherscan_api')
from dotenv import load_dotenv
import os
load_dotenv()
os.getenv('etherscan_api')
# get current time in seconds
t = time.time()
end_block = int(t)
start_block=end_block-60*60*24*30

link = "https://hub.snapshot.org/graphql"

ens_name = ""
ret_data={}
class DAO(Resource):
    def get(self,n):
        ens_name = n
        query = """query Proposals {
                    space(id: \""""+ ens_name +"""\")  {
                    strategies {
                        name
                        params
                          }
                        }
                    }"""
        r = requests.post(link, json={'query': query}).json()

        #Work on Strategy Code
        '''if r['data']['space']['strategies'][0]['params']['strategies'][0]['name']=='erc20-votes':
            print('Strategy support - ERC20')
        else:
            exit()'''


        query  = """query {
                    proposals(
                          first:100000,
                            where: {
                            space :\""""+ ens_name +"""\"
                        }
                        )
                        {
                            id
                            created
                        }

                        
                        }"""
        r = requests.post(link, json={'query': query}).json()
        list_of_proposals = []
        for id in r["data"]["proposals"]:
            list_of_proposals.append(id["id"])

        prop_count=0
        for proposal in r["data"]["proposals"]:
            if proposal['created']>start_block:
                prop_count+=1
        
        ret_data['num_of_proposals'] = prop_count
                
        list_str = str(list_of_proposals).replace("'","\"")
        query = """query {
                    votes (
                        first: 100000000                       

                        where: {
                        proposal_in: """ + list_str + """
                        }
                        orderBy: "created",
                        orderDirection: desc
                    ) {
                        created
                        voter

                    }
                    }"""
        

        r = requests.post(link, json={'query': query}).json()

                
        voter_list=[]
        for voter in r['data']['votes']:
            voter_list.append(voter['voter'])

        print(len(list(set(voter_list))))
        user_dict={}
        for voter in r['data']['votes']:
            if voter['voter'] not in user_dict and voter['created']>start_block:
                user_dict[voter['voter']] = 1
            elif voter['created']>start_block:
                user_dict[voter['voter']] += 1
                
                    
       
        ret_data['vote_count'] = len(list(set(user_dict.keys())))
        ret_data['max_vote']= max(user_dict.values())

        ret_data['votes']=user_dict
        json_object = json.dumps(ret_data, indent = 4)
        return json_object,200