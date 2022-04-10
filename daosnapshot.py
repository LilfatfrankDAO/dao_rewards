from flask_restful import Resource
import requests
import json
import pandas as pd
import os
from dotenv import load_dotenv

link = "https://hub.snapshot.org/graphql"

ens_name = ""

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
        if r['data']['space']['strategies'][0]['params']['strategies'][0]['name']=='erc20-votes':
            print('Strategy support - ERC20')
        else:
            exit()
        query  = """query {
                    proposals(
                          first:100000,
                            where: {
                            space :\""""+ ens_name +"""\"
                        }
                        )
                        {
                            id
                        }

                        
                        }"""
        r = requests.post(link, json={'query': query}).json()
        list_of_proposals = []
        for id in r["data"]["proposals"]:
            list_of_proposals.append(id["id"])
        list_str = str(list_of_proposals).replace("'","\"")
        query = """query {
                    votes (
                        first: 10000

                        where: {
                        proposal_in: """ + list_str + """
                        }
                        orderBy: "created",
                        orderDirection: desc
                    ) {
                        
                        voter

                    }
                    }"""
        etherscan_api = os.getenv('etherscan_api')
        os.getenv('etherscan_api')
        link_block = "https://api.etherscan.io/api?module=proxy&action=eth_blockNumber&apikey="+os.getenv('etherscan_api')
        end_block=int(requests.get(link_block).json()['result'],16)
        start_block=end_block-200000

        r = requests.post(link, json={'query': query}).json()
        user_dict={}
        for voter in r['data']['votes']:
            if voter['voter'] not in user_dict:
                user_dict[voter['voter']] = 1
            else:
                user_dict[voter['voter']] += 1
        json_object = json.dumps(user_dict, indent = 4)
        return json_object,200