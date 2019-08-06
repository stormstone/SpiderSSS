import requests
import pandas as pd
from bs4 import BeautifulSoup

base_url = 'https://tianchi.aliyun.com/competition/gameList'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
}

link_api = 'https://tianchi.aliyun.com/competition/proxy/api/competition/api/race/listBrief?pageNum=1&pageSize=200'
res = requests.get(link_api).json()
lst_cmpt = res['data']['list']

lst_keys = ['raceNameEn', 'raceId', 'currentSeasonStart', 'currentSeasonEnd', 'raceState',
            'state', 'season', 'teamNum', 'seasonNums', 'type',
            'currencySymbol', 'currency', 'raceType', 'briefEn', 'enHidden',
            'raceName', 'orgUrl', 'needStudent', 'brief', 'bonus']

df_res = pd.DataFrame(columns=lst_keys)
for cmpt in lst_cmpt:
    i = df_res.shape[0]
    print(i)
    for col in lst_keys:
        try:
            df_res.loc[i, col] = cmpt[col]
        except:
            pass

# df_res.columns = lst_keys
df_res.to_csv('../data/df_tianchi.csv', index=False, encoding='utf8')
