"""
ECNU 考研初试成绩自动邮件通知（曾 2019 年用于计科专业，其余未测试）
"""
import requests
import time
import re
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.header import Header


def __request(connect, **kwargs):
    try:
        res = connect.request(**kwargs)
        res.raise_for_status()
        res.encoding = res.apparent_encoding
        return res
    except:
        print('request 异常')
        return None


headers = {
    'Cookie': '',   # 需指定
    'Host': 'yjszs.ecnu.edu.cn',
    'Referer': 'https://yjszs.ecnu.edu.cn/ksxx/yjszsxxglxt_ks.asp',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}
url = 'https://yjszs.ecnu.edu.cn/ksxx/sscjxx_detail_ks.asp'

# 第三方 SMTP 服务
mail_host = ""  # 设置服务器
mail_user = ""  # 用户名
mail_pass = ""  # 口令

sender = ''     # 邮箱地址
receivers = ['']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

connect = requests.session()

while True:
    try:
        html = __request(connect, method='get', url=url, headers=headers).text
        html = BeautifulSoup(html, 'lxml')
        res = html.findAll('table')[3].findAll('tr')[1:6]

        ans = ''
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
              res[0].findAll('td')[:3][1].text.replace(' ', ''))
        for i in res:
            t = i.findAll('td')[:3]
            if re.sub('[\r\n\t ]', '', t[2].text) != '':
                ans += t[0].text.replace(' ', '') + ' ' + t[1].text.replace(' ', '') + ' ' + t[2].text.replace(' ',
                                                                                                               '') + '\n'
                print(t[0].text.replace(' ', ''), t[1].text.replace(' ', ''), t[1].text.replace(' ', ''))

        if ans != '':
            smtpObj = smtplib.SMTP()
            smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
            smtpObj.login(mail_user, mail_pass)

            message = MIMEText('成绩已公布成绩已公布成绩已公布成绩已公布成绩已公布成绩已公布成绩已公布成绩已公布成绩已公布\n\n\n\n' + ans, 'plain', 'utf-8')
            message['From'] = Header("千千", 'utf-8')
            message['To'] = Header("千千", 'utf-8')

            message['Subject'] = Header('成绩已公布', 'utf-8')

            smtpObj.sendmail(sender, receivers, message.as_string())
            print('邮件发送成功')
            break
        pass
    except:
        pass
    print('Sleep 60')
    time.sleep(60)
