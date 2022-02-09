import json
import time
import os

import requests
from bs4 import BeautifulSoup
from my_fake_useragent import UserAgent


class Ding_Robot():
    def __init__(self, dingtalk_token, msg=None, link=None, title=None):
        self.dingtalk_url = 'https://oapi.dingtalk.com/robot/send?access_token=' + dingtalk_token
        self.msg = msg
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


def get_date(link):

    req = get_web(link)
    bs = BeautifulSoup(req.content, features='html.parser')
    # Todo：这里的问卷时间不好拿啊
    date = bs.find()
    # 返回字符串数组
    return get_date


if __name__ == '__main__':

    with open('log.json','r',encoding='utf-8') as fLoad:
       web_data = json.load(fLoad)

    # Todo: 获取机器人ID
    dingtalk_token1 = os.environ["notice_robot"]    # notice_robot ‘4cf08e7a1f38b50704e1d0899999f4380625868624ba8ab891be6393abcb0d4e'
    dingtalk_token2 = os.environ["link_robot"]    # link_robot  'e0103198f33733fc61eebfb1a0b54cffc3c9beb0f45ac7804da47e9f40efaa8d'
    # dingtalk_token3 = '0e02150d02768a587b71dfc7e022019914731bb0f0c6f416faeacf33064c606d'    # error_robot

    # 部分机器人初始化
    notice_robot = Ding_Robot(dingtalk_token1, msg='HPV疫苗更新啦！速抢！')
    # error_robot = Ding_Robot(dingtalk_token3, msg='程序发生错误，请及时查看')

    for _ in range(5):
        try:
            # 页面解析失败时调用机器人提醒
            url = 'https://hospital.seu.edu.cn/'
            req = get_web(url)

            # 拿到网址并解析
            bs = BeautifulSoup(req.content, features='html.parser')
            extra_layers = bs.find_all('div', id='idy_floatdiv')


            for extra_layer in extra_layers:
                link = extra_layer.find('a')['href']
                if 'www.wenjuan.com' in link.split('/'):
                    title = get_title(link)
                    # date = get_date()
                    if link not in web_data['link_list'] or title not in web_data['title_list']:# or date not in date_list:  # 或者问卷下面的时间改了
                        # 触发提示信息
                        link_robot = Ding_Robot(dingtalk_token2, link=link, title=title)
                        print('Send notice message:', notice_robot.send_msg(mode='notice'))
                        print('Send Link:', link_robot.send_msg(mode='link'))
                        # 将新问卷链接和标题存起来
                        web_data['link_list'].append(link)
                        web_data['title_list'].append(title)
                        # print('link_list:',link_list,'title_list:',title_list,'\n')

            print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), 'Updating...')

            with open("log.json", 'w', encoding='utf-8') as f:
                json.dump(web_data, f, ensure_ascii=False, indent=4)

            break

        except:
            print('Reloading....')
            # print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), "Error:", error_robot.send_msg(mode='notice'))
