import json
import random
import time

import requests
from bs4 import BeautifulSoup
from my_fake_useragent import UserAgent


def get_title(link):
    # 找到字符串
    req = get_web(link)
    bs = BeautifulSoup(req.content, features='html.parser')
    title = bs.find('div', class_='wjintro mtop desc_begin').find('p').text
    return title


def get_web(url):
    # 伪装浏览器头部
    ua = UserAgent(family='chrome')
    res = ua.random()
    headers = {"User-Agent": res}

    req = requests.get(url, headers=headers)
    return req


def get_date(link):

    req = get_web(link)
    bs = BeautifulSoup(req.content, features='html.parser')
    date = bs.find()
    # 返回字符串数组
    return get_date

if __name__ == '__main__':
    url = 'https://www.wenjuan.com/s/iiAFf2/'
    req = get_web(url)

    # 拿到网址并解析
    bs = BeautifulSoup(req.content, features='html.parser')
    title = bs.find('div', class_='wjintro mtop desc_begin').find('p').text

    date = bs.find_all('div', class_='option_label_wrap')
    print(title)
    print(date)
