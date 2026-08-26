import pandas as pd

'''
stats to query for arithmetic
-Player
preaim
reaction_time
accuracy
kd_ratio
traded_kills_success_percentage -- percent of trading kills
accuracy_head
utility_on_death_avg -- means how long you hold on to util (higher is better performance)
--WINRATE = rounds_won > rounds_lost == count wins/losses
'''

def testing(data):
    temp = pd.Series(data)
    return temp[0]