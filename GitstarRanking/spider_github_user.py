import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_userinfo_github(username):
    user_link = 'https://github.com/' + str(username)
    r = requests.get(user_link)
    soup = BeautifulSoup(r.text)

    name = soup.find('span', itemprop="name").text
    additionalName = soup.find('span', itemprop="additionalName").text
    try:
        bio = soup.find('div', class_="p-note user-profile-bio js-user-profile-bio mb-3").text
    except:
        bio = ''
    try:
        org = soup.find('span', class_="p-org").text
    except:
        org = ''
    try:
        label = soup.find('span', class_="p-label").text
    except:
        label = ''
    try:
        email = soup.find('li', itemprop="email").text.strip()
    except:
        email = ''
    try:
        link_url = soup.find('li', itemprop="url").text.strip()
    except:
        link_url = ''
    try:
        count_ogz = len(soup.find_all('a', class_="avatar-group-item"))
    except:
        count_ogz = 0
    try:
        year_start = soup.find_all('a', class_="js-year-link filter-item px-3 mb-2 py-2 ")[-1].text
    except:
        year_start = ''

    lst_line_nav = soup.find_all('a', class_="UnderlineNav-item ")
    count_repositories = lst_line_nav[0].text.strip().split(' ')[-1]
    count_projects = lst_line_nav[1].text.strip().split(' ')[-1]
    count_stars = lst_line_nav[2].text.strip().split(' ')[-1]
    count_followers = lst_line_nav[3].text.strip().split(' ')[-1]
    count_following = lst_line_nav[4].text.strip().split(' ')[-1]

    count_contributions = soup.find('h2', class_="f4 text-normal mb-2").text.strip().split(' ')[0]

    return [name, additionalName, bio, org, label, email, link_url, count_ogz, year_start,
            count_repositories, count_projects, count_stars, count_followers, count_following,
            count_contributions]


print(get_userinfo_github('stormstone'))
