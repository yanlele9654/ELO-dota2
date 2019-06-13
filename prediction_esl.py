import dota2_api
import pandas as pd
import logging
# loading the elo_rank info
team_rank=dota2_api.get_api_json('https://api.opendota.com/api/teams')
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler('prediction_output.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

team_rank=pd.DataFrame(team_rank)
team_rank=team_rank.drop_duplicates(['name'])

team_rank=team_rank[['name','tag','rating','wins','losses']]
def elo_team(team1,team2):
    x1=team_rank.loc[team_rank['tag']==team1,['rating']]
    x2=team_rank.loc[team_rank['tag']==team2,['rating']]
    x1=x1.iloc[0][0]
    x2=x2.iloc[0][0]
    p1=1/(1+10**((x2-x1)/400))
    p2=1/(1+10**((x1-x2)/400))
    if p1 > p2:
        return('the winner team is %s'%(team1))
    else:
        return('the winner team is %s'%(team2))
team1=['Liquid','Secret','PSG.LGD']
team2=['Gambit','OG','EG']
for i in range(len(team1)):
    logger.info(elo_team(team1[i],team2[i]))
