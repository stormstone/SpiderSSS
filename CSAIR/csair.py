import datetime
import time

import requests
import pandas as pd

# 忽略：InsecureRequestWarning: Unverified HTTPS request is being made to host '127.0.0.1'.
from tqdm import tqdm

requests.packages.urllib3.disable_warnings()

url_queryCabinNumByOd = 'https://m.csair.com/CSMBP/bookProcess/happyFly/queryCabinNumByOd?APPTYPE=touch&chanel=touch&lang=zh'

header = {
    "Content-Type": "application/json",
    "Referer": "https://m.csair.com/booking_new/",
    "Host": "m.csair.com",
    "Origin": "https://m.csair.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat",
    "Cookie": ""
}


def get_total(start='2020-08-26', end='2021-01-06'):
    df_total = pd.DataFrame()

    for depDate in tqdm(pd.date_range(start=start, end=end, freq='D')):
        depDate = str(depDate)[:10]
        # 上海虹桥-广州
        body = {"dep": "SHA", "arr": "CAN", "depDate": depDate}
        res_json = requests.post(url_queryCabinNumByOd, headers=header, json=body, verify=False).json()
        try:
            totalLsv = res_json['totalLsv']
            totalBkd = res_json['totalBkd']
        except:
            print('ERROR:', depDate, " res:", res_json)
            totalLsv = -1
            totalBkd = -1
        df_total = df_total.append([[depDate, totalLsv, totalBkd]])
    df_total.columns = ['depDate', 'totalLsv', 'totalBkd']
    return df_total


if __name__ == '__main__':
    df_total = get_total()
    now_day = datetime.datetime.now().strftime("%Y-%m-%d")
    df_total.to_csv("./data/df_total_{}.csv".format(now_day), index=False)
