import json
import pandas as pd
 
# Opening JSON file
f = open('sample.json')
 
# returns JSON object as
# a dictionary
data = json.load(f)
print(list(pd.DataFrame(data.values()).value_counts().sort_index()))

import matplotlib.pyplot as plt    
import numpy as np
data_vote=np.transpose([list(range(1,len(list(pd.DataFrame(data.values()).value_counts().sort_index()))+1)),list(pd.DataFrame(data.values()).value_counts().sort_index())])
votes=pd.DataFrame(data_vote,columns=["Number of TImes","Number of Voters"])
print(votes)
import seaborn as sns
sns.histplot(data=votes,x="Number of TImes",y="Number of Voters")
plt.show()