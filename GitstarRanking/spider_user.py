import requests
from bs4 import BeautifulSoup
import pandas as pd
from spider_github_user import get_userinfo_github


# 获取所有1000个用户的用户名、排名、star数
def get_user_all():
    df_user_rank = pd.DataFrame()
    for page_num in range(10):
        print('page num:', page_num + 1)
        page_url = 'https://gitstar-ranking.com/users?page=' + str(page_num + 1)
        r = requests.get(page_url)
        soup = BeautifulSoup(r.text)
        lst_username_a = soup.find_all('a', class_="list-group-item paginated_item")
        lst_ranknum = soup.find_all('span', class_="name")
        lst_star = soup.find_all('span', class_="stargazers_count pull-right")
        for user_link, rank, star in zip(lst_username_a, lst_ranknum, lst_star):
            username = user_link.get('href')[1:]
            ranknum = rank.text.split('.')[0].strip()
            starnum = star.text.strip()
            df_user_rank = df_user_rank.append([[username, ranknum, starnum]])

    df_user_rank.columns = ['username', 'rank_num', 'star_num']
    df_user_rank.to_csv('data/df_user_rank.csv', index=False)


df_user_rank = pd.read_csv('data/df_user_rank.csv')
df_user_info = pd.DataFrame()
for username in df_user_rank['username'].values:
    print(username)
    df_user_info = df_user_info.append([get_userinfo_github(username)])

df_user_info.columns = ['name', 'additionalName', 'bio', 'org', 'label', 'email', 'link_url', 'count_ogz', 'year_start',
                        'count_repositories', 'count_projects', 'count_stars', 'count_followers', 'count_following']
df_user_info.to_csv('data/df_user_info.csv', index=False, encoding='utf8')
