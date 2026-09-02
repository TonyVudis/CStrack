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
def Goodislower(source, low, high): #JUDGEMENT OF MEANS IN FUNCTION
    if source <= low:
        return 'green', 'Good'
    elif high >= source > low:
        return 'yellow', 'Average' 
    else:
        return 'red', 'Needs Work'

def Goodishigher(source, high, low): #JUDGEMENT OF MEANS IN FUNCTION
    if source >= high:
        return 'green', 'Good'
    elif low <= source < high:
        return 'yellow', 'Average'
    else:
        return 'red', 'Needs Work'

def past_month(leetdata):
    #sifting through for needed information
    temp = pd.DataFrame(leetdata)
    last_30 = temp[temp["finished_at"] >= str(past_30_days)]
    statsstart = pd.DataFrame(last_30['stats'])
    statsmiddle = pd.DataFrame(statsstart.explode('stats').reset_index(drop=True))
    statsunpack = pd.json_normalize(statsmiddle['stats'])

    #Converting needed cols into float
    statsunpack = statsunpack[['preaim', 'reaction_time', 'accuracy', 'kd_ratio', 'accuracy_head','trade_kills_success_percentage','counter_strafing_shots_good_ratio', 'utility_on_death_avg']].round(2).astype('float64')

    #Means of needed stats
    means = statsunpack[['preaim', 'reaction_time', 'accuracy', 'kd_ratio', 'accuracy_head','trade_kills_success_percentage','counter_strafing_shots_good_ratio', 'utility_on_death_avg']].mean()

    stats=[] #STORES GOOD OR BAD VALS BASED ON MEANS
    #JUDGEMENT OF MEANS
    color, label = Goodislower(means['preaim'], 8.000, 11.000)
    stats.append({'name': 'Preaim', 'value': f"{round(means['preaim'], 2)}°", 'color': color, 'label': label})

    color, label = Goodislower(means['reaction_time'], 0.525, 0.700)
    stats.append({'name': 'Reaction time', 'value': f"{round(means['reaction_time']* 10**3)}ms", 'color': color, 'label': label})

    color, label = Goodishigher(means['accuracy'], 0.23, 0.18)
    stats.append({'name': 'Accuracy', 'value': "{:.2%}".format(means['accuracy']), 'color': color, 'label': label})

    color, label = Goodishigher(means['kd_ratio'], 1.0, 0.9)
    stats.append({'name': 'K/D', 'value': "{:.2}".format(means['kd_ratio']), 'color': color, 'label': label})

    color, label = Goodishigher(means['accuracy_head'], 0.28, 0.18)
    stats.append({'name': 'Headshot Average', 'value': "{:.2%}".format(means['accuracy_head']), 'color': color, 'label': label})

    color, label = Goodishigher(means['trade_kills_success_percentage'], 0.5, 0.35)
    stats.append({'name': 'Successful Trading', 'value': "{:.2%}".format(means['trade_kills_success_percentage']), 'color': color, 'label': label})

    color, label = Goodishigher(means['counter_strafing_shots_good_ratio'], 0.87, 0.8)
    stats.append({'name': 'Counter Strafing', 'value': "{:.2%}".format(means['counter_strafing_shots_good_ratio']), 'color': color, 'label': label})

    color, label = Goodislower(means['utility_on_death_avg'], 200.0, 350.0)
    stats.append({'name': 'Utility', 'value': "{:.5}".format(means['utility_on_death_avg']), 'color': color, 'label': label})
  
    html_display = statsunpack.to_html(max_cols = None, max_rows= None)
    return stats

def steamaccsort(steamdata):
    accinfo = pd.DataFrame(steamdata['response']['players'])
    steaminfo = ({'Name': accinfo['personaname'].iloc[0], 'Avatar': accinfo['avatarfull'].iloc[0]})

    return steaminfo
    