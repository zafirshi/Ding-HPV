# Ding-HPV

## 1. 项目说明

本项目使用Python爬虫，爬取[SEU校医院](https://hospital.seu.edu.cn/)的HPV疫苗填写问卷，通过钉钉群机器人发送提醒消息和问卷链接

## 2. 使用设置

### 2.1 机器人配置

使用本项目前，需要配置钉钉的群聊机器人，具体配置方法如下：

PC端钉钉 > 新手体验群 > 群设置 > 智能群助手 > 添加机器人 > 自定义

需要添加两个机器人：名字分别为`notice_robot`和`link_robot`

1. notice_robot：安全设置选择`自定义关键字`，填`HPV`，然后下一步复制Webhook。

2. link_robot:安全设置选择`自定义关键字`，填两个`问卷`和`链接`，然后下一步复制Webhook。

### 2.2 代码配置

将两个钉钉机器人Webhook的后面token，分别复制在代码的`dingtalk_token1`(对应notice_robot变量)和`dingtalk_token2`(对应link_robot变量)中

最后`time.sleep()`中可以调整每次抓取的时间，默认30min一次，建议不要抓太快

### 2.3 运行逻辑

代码运行后，会先发送两条消息提醒，以用作初始化。

每隔一段时间抓取后，与存储的上一条作比对，如果**新增问卷链接** 或者**旧问卷标题被更新** ，

就会触发机器人提醒

### 2.4 Todo

- [ ] 爬取数据的时候，可以使用ip代理伪装

- [ ] 链接应该都是在工作时间8：00~18：00更新，可以定时段抓取

- [ ] 其他待测试情况

## 3.环境部署

本项目环境已存放在`env.yml`文件中，可以使用如下命令创建本项目环境：

```Bash
conda env create -f env.yml
```


> PS: 创建前需要进入该文件，修改最下面文件目录到本地conda环境中

**建议将本项目部署在VPS或者树莓派等全天运行的硬件上** 

服务器上后台运行`main.py`并打印输出日志文件到main.log:

```bash
nohup python -u main.py > main.log 2>&1 &
```

## 4. 参考链接：

- 添加自定义机器人：

[https://www.dingtalk.com/qidian/help-detail-20781541.html](https://www.dingtalk.com/qidian/help-detail-20781541.html)

- 自定义机器人接入API：

[https://developers.dingtalk.com/document/robots/custom-robot-access#section-e4x-4y8-9k0](https://developers.dingtalk.com/document/robots/custom-robot-access#section-e4x-4y8-9k0)

- 爬虫的基本知识：

[https://segmentfault.com/u/bersder###](https://segmentfault.com/u/bersder###)

- 可以尝试的代理ip池：

[https://blog.csdn.net/weixin_51852924/article/details/120019488](https://blog.csdn.net/weixin_51852924/article/details/120019488)

[https://github.com/Python3WebSpider/ProxyPool](https://github.com/Python3WebSpider/ProxyPool)

- 相似实例教程：

[https://www.bilibili.com/s/video/BV1ob411K7B3](https://www.bilibili.com/s/video/BV1ob411K7B3)

