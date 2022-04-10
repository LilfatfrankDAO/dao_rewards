from dotenv import load_dotenv
import os
load_dotenv()
os.getenv('etherscan_api')
print(os.getenv('etherscan_api'))