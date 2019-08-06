import requests
import pandas as pd

link_json = 'http://www.pkbigdata.com/common/getNewCmptList.json'
lst_keys = ['rewardType', 'icon', 'type', 'technologyLabel', 'customPage', 'startTime', 'id', 'state',
            'introduction', 'HostName', 'reward', 'totalUserNumber', 'level', 'mold', 'industryLabel',
            'name', 'miniAppState', 'endTime']

df_res = pd.DataFrame()
hasNextPage = True  # 是否有下一页
page = 1
while hasNextPage:
    print('page:', page)
    res = requests.post(link_json, params={'page': page, 'pageSize': 10}).json()
    page += 1
    hasNextPage = res['data']['cmptList']['hasNextPage']
    lst_cmpt = res['data']['cmptList']['list']
    for cmpt in lst_cmpt:
        df_res = df_res.append([[i for i in cmpt.values()]])

df_res.columns = lst_keys
df_res.to_csv('../data/df_dc.csv', index=False, encoding='utf8')
