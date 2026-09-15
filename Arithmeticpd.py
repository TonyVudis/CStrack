import pandas as pd
from datetime import date, timedelta
from sync import pull_leetify_prof
today = date.today()
past_30_days = today - timedelta(days=30)

from flask import Flask, redirect, flash, url_for
app = Flask(__name__)

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

recommend = {
    'preaim': {
        'text': 'This measures how close your crosshair is to an enemy as you peek', 
        'help': ['-Try aiming through walls and line up your crosshair headheight on common holding sights and corners',
                      '-Peek with distance from walls if you can.', 
                      '-Having good counter-strafing fundamentals help'
                      '-Good workshop maps for practice: lmtlss Prefire Training and 5E_Aimhub'],
        'gif': 'preaim.gif'    
    },
    'reaction_time': {
        'text': 'This measures how fast you react to enemies', 
        'help': ['-Try to anticipate where enemies could be using audio queues and common timings',
                '-Strong crosshair placement and counter strafing will help',
                '-Good workshop maps for practice: Fast Aim Reflex and Aim_Rush'],
        'gif': 'reaction_time.gif'
    },
    'accuracy': {
        'text': 'This measures how often you hit an enemy', 
        'help': ['-To counterstrafe, you should completely stop using the opposite key either A or D then shoot',
                '-Avoid moving and shooting at the same time enless up close using certain weapons like pistols and some smgs/shotguns',
                '-Burst/tap at range and spray when close up and practice your spray patterns',
                '-Good workshop maps for practice: CS2 Labs and Aim Botz'],
        'gif': 'accuracy.gif'
    },
    'kd_ratio': {
        'text': 'This measures your kill to death ratio', 
        'help': ['-This ends up being a combination of the statistics you see here such as headshot accuracy, reaction time and preaim',
                '-Try warming up before going into a game using deathmatch or a workshop map',
                '-Trade your teammates when you can and pick 1v1 fights',
                '-Good workshop maps for practice: Aim_Rush and Fast Warmup - Bot Training'],
        'gif': 'kd_ratio.gif'
    },
    'accuracy_head': {
        'text': 'This measures how often your shots hit an enemy head', 
        'help': ['-Counterstrafing is a huge part of head shots so make sure to be solid on that first',
                '-Aim headheight constantly even before fights so you dont need to micro adjust',
                '-Aim for upper neck or the head preferably',
                '-Good workshop maps for practice: Aim Botz and Aim_Rush'],
        'gif': 'accuracy_head.gif'
    },
    'trade_kills_success_percentage': {
        'text': 'This measures how often you avenge a teammate soon after they die', 
        'help': ['-Try to be more of a team player and pay attention to what your teammates are holding and peeking',
                '-When a teammate is entry fragging try to avenge them if they are killed by an enemy',
                '-Dont body block and preaim where the enemy is shooting from at your teammate'],
        'gif': 'trade_kills_success_percentage.gif'
    },
    'counter_strafing_shots_good_ratio': {
        'text': 'This measures how good you are at counterstrafing to hit an enemy', 
        'help': ['-To counterstrafe, you should completely stop using the opposite key either A or D then shoot',
                '-Clear corners and peek and preaim at the most common angles one by one',
                '-If far away tap or burst then reposition and repeat',
                '-Good workshop maps for practice: Yprac Prefire Maps and Aim Botz'],
        'gif': 'counter_strafing_shots_good_ratio.gif'
    },
    'utility_on_death_avg': {
        'text': 'This measures how much utility you die with each round on average', 
        'help': ['-Try to stay alive while activly using your util to help your team entry or hold down sites',
                '-Learn basic lineups the premier maps(See the Lineups tab in the top right)'],
        'gif': 'utility_on_death_avg.gif'
    },
}


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
    stats.append({'name': 'Preaim', 'value': f"{round(means['preaim'], 2)}°", 'color': color, 'label': label, 'recommendation' : recommend.get(('preaim'), '')})

    color, label = Goodislower(means['reaction_time'], 0.525, 0.700)
    stats.append({'name': 'Reaction time', 'value': f"{round(means['reaction_time']* 10**3)}ms", 'color': color, 'label': label, 'recommendation' : recommend.get(('reaction_time'), '')})

    color, label = Goodishigher(means['accuracy'], 0.23, 0.18)
    stats.append({'name': 'Accuracy', 'value': "{:.2%}".format(means['accuracy']), 'color': color, 'label': label, 'recommendation' : recommend.get(('accuracy'), '')})

    color, label = Goodishigher(means['kd_ratio'], 1.0, 0.9)
    stats.append({'name': 'K/D', 'value': "{:.2}".format(means['kd_ratio']), 'color': color, 'label': label, 'recommendation' : recommend.get(('kd_ratio'), '')})

    color, label = Goodishigher(means['accuracy_head'], 0.28, 0.18)
    stats.append({'name': 'Headshot Average', 'value': "{:.2%}".format(means['accuracy_head']), 'color': color, 'label': label, 'recommendation' : recommend.get(('accuracy_head'), '')})

    color, label = Goodishigher(means['trade_kills_success_percentage'], 0.5, 0.35)
    stats.append({'name': 'Successful Trading', 'value': "{:.2%}".format(means['trade_kills_success_percentage']), 'color': color, 'label': label, 'recommendation' : recommend.get(('trade_kills_success_percentage'), '')})

    color, label = Goodishigher(means['counter_strafing_shots_good_ratio'], 0.87, 0.8)
    stats.append({'name': 'Counter Strafing', 'value': "{:.2%}".format(means['counter_strafing_shots_good_ratio']), 'color': color, 'label': label, 'recommendation' : recommend.get(('counter_strafing_shots_good_ratio'), '')})

    color, label = Goodislower(means['utility_on_death_avg'], 200.0, 350.0)
    stats.append({'name': 'Utility', 'value': "{:.5}".format(means['utility_on_death_avg']), 'color': color, 'label': label, 'recommendation' : recommend.get(('utility_on_death_avg'), '')})
  
    html_display = statsunpack.to_html(max_cols = None, max_rows= None)
    return stats

def steamaccsort(steamdata):
    players_list = steamdata.get('response', {}).get('players', [])
    accinfo = pd.DataFrame(players_list)
    steaminfo = ({'Name': accinfo['personaname'].iloc[0], 'Avatar': accinfo['avatarfull'].iloc[0]})

    return steaminfo
    