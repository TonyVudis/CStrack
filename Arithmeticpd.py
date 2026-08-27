import pandas as pd
from datetime import date, timedelta
today = date.today()
past_30_days = today - timedelta(days=30)
'''
stats to query for arithmetic
-Player
preaim
reaction_time
accuracy
kd_ratio
trade_kills_success_percentage -- percent of trading kills
accuracy_head
counter_strafing_shots_good_ratio
utility_on_death_avg -- means how long you hold on to util (higher is better performance)
--WINRATE = rounds_won > rounds_lost == count wins/losses
'''

def past_month(data):
    #sifting through for needed information
    temp = pd.DataFrame(data)
    last_30 = temp[temp["finished_at"] >= str(past_30_days)]
    statsstart = pd.DataFrame(last_30['stats'])
    statsmiddle = pd.DataFrame(statsstart.explode('stats').reset_index(drop=True))
    statsunpack = pd.json_normalize(statsmiddle['stats'])

    #Converting needed cols into float
    statsunpack = statsunpack[['preaim', 'reaction_time', 'accuracy', 'kd_ratio', 'accuracy_head','trade_kills_success_percentage','counter_strafing_shots_good_ratio', 'utility_on_death_avg']].round(4).astype('float64')

    #Means of needed stats
    means = statsunpack[['preaim', 'reaction_time', 'accuracy', 'kd_ratio', 'accuracy_head','trade_kills_success_percentage','counter_strafing_shots_good_ratio', 'utility_on_death_avg']].mean()
    html_display = statsunpack.to_html(max_cols = None, max_rows= None)
    return means
    