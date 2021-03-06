# encoding:utf-8
'''
author: sixseven
topic: 爬取裁判文书网
date: 2018-04-17
contact: 2557692481@qq.com

modified: ztcooper
2018-04-24
cotact: 1060214139@qq.com

获得API数据
'''
import requests
from urllib import parse
import execjs
# import json
from random import choice
from settings import Settings


class GetAPI(object):
    def __init__(self):
        self.session = requests.Session()
        self.s = Settings().setting
        self.sc = Settings().shortcut
        self.u = Settings().user_agents

    def get_guid(self):
        # 获取guid参数
        js1 = '''
            function getGuid() {
                var guid = createGuid() + createGuid() + "-" + createGuid() + "-" + createGuid() + createGuid() + "-" + createGuid() + createGuid() + createGuid(); //CreateGuid();
                return guid;
            }
            var createGuid = function () {
                return (((1 + Math.random()) * 0x10000) | 0).toString(16).substring(1);
            }
        '''
        ctx1 = execjs.compile(js1)
        guid = (ctx1.call("getGuid"))
        return guid

    def get_number(self, guid):
        # 获取number
        codeUrl = "http://wenshu.court.gov.cn/ValiCode/GetCode"
        data = {
            'guid': guid
        }
        headers = {
            'Host': 'wenshu.court.gov.cn',
            'Origin': 'http://wenshu.court.gov.cn',
            'Referer': 'http://wenshu.court.gov.cn/',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': choice(self.u),
        }
        req1 = self.session.post(codeUrl, data=data, headers=headers)
        number = req1.text
        return number

    def get_vjkl5(self, guid, number, Param):
        # 获取cookie中的vjkl5
        shortcut = self.sc["%s" % Param.split(":")[0]] 
        url1 = "http://wenshu.court.gov.cn/list/list/?sorttype=1&number=" + number + \
            "&guid=" + guid + "&conditions=searchWord+" + shortcut + "++" + \
            parse.quote(Param)
        Referer1 = url1
        headers1 = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Host": "wenshu.court.gov.cn",
            "Proxy-Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": choice(self.u),
        }
        req1 = self.session.get(url=url1, headers=headers1, timeout=10)
        try:
            vjkl5 = req1.cookies["vjkl5"]
            return vjkl5
        except:
            return self.get_vjkl5(guid, number, Param)

    def get_vl5x(self, vjkl5):
        # 根据vjkl5获取参数vl5x
        js = ""
        fp1 = open('./sha1.js')
        js += fp1.read()
        fp1.close()
        fp2 = open('./md5.js')
        js += fp2.read()
        fp2.close()
        fp3 = open('./base64.js')
        js += fp3.read()
        fp3.close()
        fp4 = open('./vl5x.js')
        js += fp4.read()
        fp4.close()
        ctx2 = execjs.compile(js)
        vl5x = (ctx2.call('vl5x', vjkl5))
        return vl5x

    def get_data(self, Index):
        Param = self.s["Param"]
        Page = self.s["Page"]
        Order = self.s["Order"]
        Direction = self.s["Direction"]
        guid = self.get_guid()
        number = self.get_number(guid)
        vjkl5 = self.get_vjkl5(guid, number, Param)
        vl5x = self.get_vl5x(vjkl5)

        # 获取数据
        url2 = "http://wenshu.court.gov.cn/List/ListContent"
        headers2 = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Host": "wenshu.court.gov.cn",
            "Origin": "http://wenshu.court.gov.cn",
            "Proxy-Connection": "keep-alive",
            # "Referer":Referer1,
            "User-Agent": choice(self.u),
            "X-Requested-With": "XMLHttpRequest"
        }
        data = {
            "Param": Param,
            "Index": Index,
            "Page": Page,
            "Order": Order,
            "Direction": Direction,
            "vl5x": vl5x,
            "number": number,
            "guid": guid
        }
        req2 = self.session.post(url=url2, headers=headers2, params=data)
        return req2.text


'''
def test():
    Param = "全文检索:*"  # 搜索关键字
    Index = 1  # 第几页
    Page = 20  # 每页几条
    Order = "法院层级"  # 排序标准
    Direction = "asc"  # asc正序 desc倒序
    s = GetAPI()
    result = s.get_data(Param, Index, Page, Order, Direction)
    with open('result.txt', 'w') as f:
        f.write(result)


if __name__ == '__main__':
    test()
'''
