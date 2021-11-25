import json
import time

import requests
from bs4 import BeautifulSoup
from my_fake_useragent import UserAgent


class Ding_Robot():
    def __init__(self, dingtalk_token, link=None, title=None):
        self.dingtalk_url = 'https://oapi.dingtalk.com/robot/send?access_token=' + dingtalk_token
        self.msg = 'HPV疫苗更新啦！速抢！'
        self.header = {'Content-Type': 'application/json'}
        self.link = link
        self.title = title

    def send_msg(self, mode='notice', tries=5):
        if mode == 'notice':
            data = {
                "msgtype": "text",
                "text": {
                    "content": self.msg
                },
                "at": {
                    "isAtAll": True
                }
            }
        elif mode == 'link':
            data = {
                "msgtype": "link",
                "link": {
                    "text": self.title + "问卷获取可能存在延时，请尽快填写",
                    "title": "HPV校医院问卷链接",
                    "picUrl": "",
                    "messageUrl": self.link
                }
            }

        for _ in range(tries):
            try:
                r = requests.post(self.dingtalk_url,
                                  data=json.dumps(data), headers=self.header).json()
                # print(r)
                if r["errcode"] == 0:
                    return True
            except:
                pass
            print('Retrying...')
            time.sleep(5)
        return False


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

    # Todo: 可以设置代理ip
    req = requests.get(url, headers=headers)
    return req


if __name__ == '__main__':

    link_list = []  # 用来存每次问卷的链接
    title_list = []  # 用来存放每次问卷的标题

    while True:
        url = 'https://hospital.seu.edu.cn/'
        req = get_web(url)

        # 拿到网址并解析
        bs = BeautifulSoup(req.content, features='html.parser')
        extra_layers = bs.find_all('div', id='idy_floatdiv')

        for extra_layer in extra_layers:
            link = extra_layer.find('a')['href']
            if 'www.wenjuan.com' in link.split('/'):
                title = get_title(link)
                if link not in link_list or title not in title_list:
                    # 触发提示信息
                    # Todo: 设置两个机器人，并替换掉下面的token
                    dingtalk_token1 = '4cf08e7a1f38b50704e1d0899999f4380625868624ba8ab891be6393abcb0d4e'
                    dingtalk_token2 = 'e0103198f33733fc61eebfb1a0b54cffc3c9beb0f45ac7804da47e9f40efaa8d'
                    notice_robot = Ding_Robot(dingtalk_token1)
                    link_robot = Ding_Robot(dingtalk_token2, link, title)
                    print('Send notice message:', notice_robot.send_msg(mode='notice'))
                    print('Send Link:', link_robot.send_msg(mode='link'))
                    # 将新问卷链接和标题存起来
                    link_list.append(link)
                    title_list.append(title)
                    # print('link_list:',link_list,'title_list:',title_list,'\n')

        print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()),'Sleep 30min...')
        time.sleep(1800)
