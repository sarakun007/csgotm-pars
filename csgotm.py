import time

import requests
import json
from bs4 import BeautifulSoup

# URL = 'https://market.csgo.com/ajax/price/all/all/365/1/56/0;500000/all/all/all?sd=asc'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    'accept': '*/*'}

# URL2 = 'https://steamcommunity.com/market/search/render/?query=&start=0&count=10&search_descriptions=0&sort_column=price&sort_dir=asc&appid=730&category_730_ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_StickerCapsule%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Type%5B%5D=tag_CSGO_Type_Knife'

st, fn = 217, 221
st2, fn2 = 85, 96


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def parse():
    # html = get_html(URL)
    # html2 = get_html(URL2)

    steam_price = dict()
    for p in range(st*10, fn*10+1, 10):
        steam = []
        URL2 = f'https://steamcommunity.com/market/search/render/?query=&start={p}&count=10&search_descriptions=0&sort_column=price&sort_dir=asc&appid=730&category_730_ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_StickerCapsule%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Type%5B%5D=tag_CSGO_Type_Knife'
        html2 = get_html(URL2)
        a = html2.text.split('data-currency=\\"1\\">')
        for i in range(1, len(a)):
            steam.append(a[i].split('"'))

        for i in range(len(steam)):
            s0 = float(steam[i][0].replace('USD<\/span>\\r\\n\\t\\t\\t\\t\\t<span class=\\', '').replace('$', '').strip().replace(',',''))
            s18 = steam[i][18].replace('<\/span>\\r\\n\\t\\t\\t<br\/>\\r\\n\\t\\t\\t<span class=\\', '').replace('>',
                                                                                                                 '').strip()
            steam_price[s18] = s0
    # for n, p in steam_price.items():
    #     print(p, n)

    for p in range(st2, fn2):
        URL = f'https://market.csgo.com/ajax/price/all/all/365/{p}/56/0;500000/all/all/all?sd=asc'
        html = get_html(URL)
        knife = html.text
        s = knife.split(',')
        csgotm_price = dict()
        for i in range(len(s) - 7):
            if '★' in s[i] and '[' not in s[i + 1]:
                s6 = s[i + 6].replace('"', ' ').replace(' ]', '').strip()
                s1 = (float(s[i + 1]) / 61).__round__(2)
                if s6 not in csgotm_price:
                    csgotm_price[s6] = s1
    # for n, p in csgotm_price.items():
    #     print(p, n)

    for i in steam_price.keys():
        for j in csgotm_price.keys():
            if i == j and steam_price[i] / csgotm_price[j] >=1.2:
                print(i, steam_price[i], csgotm_price[i])
    print(len((steam_price)), len(csgotm_price))


while True:
    parse()
    time.sleep(40)
