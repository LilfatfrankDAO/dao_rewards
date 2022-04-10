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
#print(os.getenv('etherscan_api'))

# get current time in seconds
t = time.time()
end_block = int(t)
start_block=end_block-60*60*24*30

ens_name = "uniswap"

#1. Get Strategy
link = "https://hub.snapshot.org/graphql"


query = """query Proposals {
      space(id: \""""+ ens_name +"""\")  {
              strategies {
                name
                  params
                          }
                        }
                    }"""


r = requests.post(link, json={'query': query}).json()
'''
if r['data']['space']['strategies'][0]['params']['strategies'][0]['name']=='erc20-votes':

    print('Strategy support - ERC20')

else:
    exit()
'''
#2. Get Proposal list Base

link = "https://hub.snapshot.org/graphql"
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

print("Proposals in the past month: ")
for proposal in r["data"]["proposals"]:
  if proposal['created']>start_block:
    print(proposal)
list_str = str(list_of_proposals).replace("'","\"")



#Get Voters list of entire DAO 
query = """query {
votes (
    first: 1000000000

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

'''

link_block = "https://api.etherscan.io/api?module=proxy&action=eth_blockNumber&apikey="+os.getenv('etherscan_api')

end_block=int(requests.get(link_block).json()['result'],16)'''


# get current time in seconds
t = time.time()
end_block = int(t)
start_block=end_block-60*60*24*30

user_dict={}
for voter in r['data']['votes']:
    if voter['voter'] not in user_dict and voter['created']>start_block:
        user_dict[voter['voter']] = 1
    elif voter['created']>start_block:
        user_dict[voter['voter']] += 1


print("Voter Count for the past month")
print(len(list(set(user_dict.keys()))))


print("Max Vote Count in the past month")
print(max(user_dict.values()))
json_object = json.dumps(user_dict, indent = 4) 
with open("sample.json", "w") as outfile:
    json.dump(user_dict, outfile)


