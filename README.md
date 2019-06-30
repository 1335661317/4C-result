## CCCC - 中国高校计算机大赛 成绩抓取+排序
### 环境
    编译语言：python
    版本号：  python3.4
    基于 urllib && requests && BeautifulSoup

### 功能
- 抓取成绩
- 可按照 名次/名称/总分 进行排序

### 使用方法
    安装python3.4及所需的requests urllib bs4
    
    Ubuntu：
        sudo apt-get install python3.4
        sudo apt-get install python-pip
        pip install bs4
        pip install requests
        python main.py
        
    Windows：
        download && install python3.4
        cmd
        cd c:\Python34\Scripts
        pip3.4.exe install bs4
        pip3.4.exe install requests
        python main.py
    
    1、输入所要抓取的contest名称（如 https://www.patest.cn/contests/2016gplt-0 中的 2016gplt-0）
    2、输入账号名称（比赛结束之后任意账号都可行）
    3、输入密码（比赛结束之后任意密码都可行）
    4、输入所要提取的关键字（如zju）
    5、输入要保存的文件名称（如result.html）
    
    搞定~

## 蓝桥杯做题情况抓取

- user 为指定用户 id
- cookie 为教师账户登录以后所获得的

最终保存为 xls 表格

## 甘肃教师学苑自动阅读文章

idList 为要阅读的文章 id

## ECNU 考研初试成绩自动邮件通知

- cookie 需自行指定
- mail_host smtp 服务器地址
- mail_user smtp 用户名
- mail_pass smtp 密码
- sender 发件人地址
- receivers 收件人地址

