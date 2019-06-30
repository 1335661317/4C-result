# -*- coding:utf-8 -*-
"""
抓取指定用户的做题情况（需要教师账户）
"""
import urllib
import urllib.request
import urllib.parse
import xlwt
import json
import re
import queue

user = [111835, 131937, 111834, 69912, 111841, 111843, 111836, 106745, 72369, 144273, 111842, 111849, 111844, 111838,
        105647, 132293, 140441, 111833, 111831, 111600, 111839, 76970, 106206, 72372, 137315, 75701, 68616, 111687,
        111845, 69133, 132300, 121384, 72367, 132416, 132319, 93709, 111750, 69456, 72506, 73826, 111837,76972
        ]
todo_queue = queue.Queue()
filter_html = re.compile(r'<[^>]+>', re.S)


class LanQiao(object):
    """
    This is a class.
    """
    result_set_url = 'http://lx.lanqiao.cn/problem.TrainProblems.dt'
    header = {}
    start_pid = 0
    end_pid = 407 + 1

    # 构造函数，设置cookie
    def __init__(self, cookie):
        self.header['Cookie'] = cookie

        self.xls = xlwt.Workbook()
        self.sheet = self.xls.add_sheet('sheet')
        # 添加excel表头
        js = self.get_to_json()
        if js != -1:
            self.create_head(js)

    # 建立excel表头
    def create_head(self, js):
        print("create head -ing")
        for i in range(self.start_pid, self.end_pid):
            self.sheet.write(i + 1, 0, str(i))
            self.sheet.write(i + 1, 1, js.get(str(i)).get('gpid'))
            self.sheet.write(i + 1, 2, js.get(str(i)).get('title'))

    # 获取网页信息，返回转换为json的对象
    def get_to_json(self, uid=''):
        uid = str(uid)
        req = urllib.request.Request(url=self.result_set_url + '?userid=' + uid, headers=self.header)
        try:
            result = urllib.request.urlopen(req).read().decode('utf-8')
            return json.loads(result)
        except Exception:
            print('Error:' + uid + ' move to [Todo Queue]')
            # todo_queue.put(uid)
            return self.get_to_json(uid)
            # return -1

    # 设置单元格背景色
    def set_style(self, colour):
        return xlwt.easyxf(
            'pattern: pattern solid, fore_colour %s;' % colour
        )

    def add_new(self, index, js):
        ac_num = 0
        for i in range(self.start_pid, self.end_pid):
            res = filter_html.sub('', js.get(str(i)).get('lanqiaostatus')).strip()
            if res == "未打开" or res == "已打开":
                continue
            if res == "正确":
                ac_num += 1
                self.sheet.write(i + 1, index, res, self.set_style('bright_green'))
            else:
                self.sheet.write(i + 1, index, res, self.set_style('red'))
        self.sheet.write(0, index, js.get('username') + ' (' + str(ac_num) + ')')

    def create_xls(self, path):
        id = 3
        for i in user:
            todo_queue.put(str(i))
        while not todo_queue.empty():
            uid = todo_queue.get()
            print('Working:' + uid + ' waiting:' + str(todo_queue.qsize()))
            js = self.get_to_json(uid)
            if js != -1:
                self.add_new(id, js)
                id += 1
        self.xls.save(path)


if __name__ == '__main__':
    cookie = 'JSESSIONID=294D9D3221596A3A46D750529B0DDABA; _SESSIONKEY=6PCAYHN8L728GP4C6U34; _TOKEN=D63780D17FB495745434AA68AC602CCE94C9B443130A3D6F4A52DFF864AEBE1A715BEA5D87A782E3C182A8E41BBE7B8448515CB1105D450A34AA01BCE56C3C839945BD4680A79FE8BA51DD63F84B778C; tsinsenu=17052; tsinsent=1486616840746'
    ans = LanQiao(cookie)
    ans.create_xls(r"C:/Users/qianqian/Desktop/1.xls")
    print("end")
