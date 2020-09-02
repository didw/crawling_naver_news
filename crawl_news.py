import os
import time
import requests
import encodings
import datetime
import random
from multiprocessing import Process
from tqdm import tqdm
from bs4 import BeautifulSoup

session = requests.session()
session.proxies = {}

session.proxies['http'] = 'socks5h://localhost:9050'
session.proxies['https'] = 'socks5h://localhost:9050'

headers = {'User-Agent':'Mozilla/5.0'}

def get_news_list(date, page_num):
    url = f"https://news.naver.com/main/list.nhn?mode=LSD&mid=sec&listType=title&sid1=001&date={date}&page={page_num}"

    res = []
    raw = requests.get(url, headers=headers)
    html = BeautifulSoup(raw.text, 'html.parser')
    articles_group = html.select("ul.type02 > li")
    for articles in articles_group:
        for a in articles.find_all('a', href=True):
            res.append([a.text, a['href']])

    final = False
    if len(res) < 50:
        final = True
    return res, final


def get_news(url):
    raw = requests.get(url, headers=headers)
    html = BeautifulSoup(raw.text, 'html.parser')
    try:
        title = html.select("#articleTitle")
        if isinstance(title, list):
            title = title[0].text
        text = html.select("#articleBodyContents")
        if isinstance(text, list):
            text = text[0].text
    except Exception as _e:
        return title, html.text
    return title, text


def save_news(date, fname, title, text):
    if not os.path.exists(os.path.dirname(fname)):
        os.makedirs(os.path.dirname(fname))
    with open(fname, 'w', encoding='utf-8') as f:
        f.write("{}\n\n".format(title))
        f.write(text.strip())
        f.write("\n")


def get_news_to_save(url, date, fname):
    try:
        title, text = get_news(url)
        save_news(date, fname, title, text)
    except Exception as e:
        print(e)


def check_current_ip():
    url = "https://icanhazip.com"
    raw = session.get(url, headers=headers)
    html = BeautifulSoup(raw.text, 'html.parser')
    ip = html.text.strip()
    print(f"current ip : {ip}")


def change_ip():
    try:
        os.system("sudo service tor restart")
        time.sleep(5)
        check_current_ip()
    except Exception as e:
        print(e)


def get_all_news_by_date(date):
    page_limit = 1000
    idx = 0
    prev_news_list = []
    cur_dtime = datetime.datetime.now()
    if datetime.time(8, 0) <= cur_dtime.time() <= datetime.time(18, 30) and cur_dtime.weekday() in [0,1,2,3,4]:
        max_ps = 50
        sleep_time = 0.1
    else:
        max_ps = 500
        sleep_time = 0.001

    ps = []
    if os.path.exists(f"news/{date}"):
        return
    change_ip()
    os.makedirs(f"news/{date}")
    for page in tqdm(range(1, page_limit)):
        if max_ps == 500 and page % 100 == 0:
            time.sleep(5)
            change_ip()
        try:
            news_list, final = get_news_list(date, page)
        except Exception as e:
            print(e)
            time.sleep(5)
            change_ip()
            continue
        if news_list == prev_news_list:
            break
        prev_news_list = news_list
        for _title, url in news_list:
            idx += 1
            fname = f"news/{date}/{idx}.txt"
            if os.path.exists(fname):
                continue
            p = Process(target=get_news_to_save, args=(url, date, fname))
            t = random.randint(1, 10)
            time.sleep(sleep_time + t/1000)
            p.start()
            ps.append(p)
            while len(ps) > max_ps:
                ps[0].join()
                del ps[0]
        if final:
            break
    for p in ps:
        p.join()


def main():
    cdate = datetime.datetime.now()
    edate = datetime.datetime(1990,1,1)
    while cdate >= edate:
        print(f"crawling {cdate}")
        get_all_news_by_date(cdate.strftime("%Y%m%d"))
        cdate -= datetime.timedelta(days=1)


if __name__ == '__main__':
    main()
