"""
甘肃教师学苑，自动阅读文章
"""

import requests
import time


def __request(connect, **kwargs):
    '''
    request 方法封装，预处理
    :param connect:
    :param kwargs:
    :return: Response 对象，出错返回 None
    '''
    try:
        res = connect.request(**kwargs)
        res.raise_for_status()
        res.encoding = res.apparent_encoding
        return res
    except:
        print('request 异常')
        return None


idList = ['180404175401719240003', '180404175343904240002', '180404175327258240001', '180402152303292240694',
          '180402152245430240693', '180402152220111240692', '180402152203559240691', '180330152922373240139',
          '180330152906742240138', '180330152838771240136', '180330152804357240135', '180326215222247240553',
          '180326215156632240552', '180326215132686240551', '18032621510724240550', '180323162930268240132',
          '180323162911314240131', '180323162848272240130', '180323162829521240129', '180319214457332240093',
          '180319214432965240092', '180319214400392240091', '180319214338677240090', '180316180515659240651',
          '180316163334372240644', '180316163321424240643', '180316163256635240642', '180312205541325240014',
          '180312205523447240013', '180312205448222240012', '180312160929439240007']

end_list = []

headers = {
    'Cookie': 'Cookie',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
}

connect = requests.session()

preurl = 'http://rwsy.gsres.cn/wx/read.htm?id=%s'
print('Start!!!')

le = len(idList)
i = 0
while i < le:
    try:
        url = preurl % idList[i]
        html = __request(connect, method='get', url=url, headers=headers).text
        if html.find('您已阅读，无需重复阅读') != -1 or html.find('已阅成功') != -1:
            print(url + ' 已阅成功')
            end_list.append(idList[i])
            i = i + 1
        elif html.find('您阅读过于频繁，请稍候再试，谢谢！') != -1:
            print(url + ' 阅读频繁')
        elif html.find('您已达到每日阅读上限，请明日继续学习') != -1:
            print('阅读达到上限')
            for i in end_list:
                try:
                    idList.remove(i)
                except:
                    pass
            print(idList)
            break
        time.sleep(120)
    except:
        print(preurl % idList[i] + ' 请求失败')

print('The End')
