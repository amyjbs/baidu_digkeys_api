# -*- coding: utf-8 -*-
import requests
import json,sys
import time
reload(sys)
sys.setdefaultencoding("utf-8")

def get_result_data(key, uconfig, cookie, retry=3):
    """获取关键词查询结果数据
    :param key: 要查询的关键词
    :param uconfig: 用户配置信息
    :param cookie: cookie登录信息
    :param retry: 链接过程失败重试次数
    :return: 返回json类型数据以及错误信息
    """
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': cookie,
        'Host': 'fengchao.baidu.com',
        'Origin': 'http://fengchao.baidu.com',
        'Referer': 'http://fengchao.baidu.com/nirvana/main.html?userid=%s' % uconfig['userid'],
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 '
        '(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    }
    query = 'http://fengchao.baidu.com/nirvana/request.ajax?'\
            'path=jupiter/GET/kr/word&reqid=%s' % uconfig['reqid']

    params = {
        "logid": -1,
        "query": key,
        "querySessions": [key],
        "querytype": 1,
        "regions": "0",
        "device": 0,
        "rgfilter": 1,
        "entry": "kr_wordlist_addwords",
        "planid": "0",
        "unitid": "0",
        "needAutounit": False,
        "filterAccountWord": True,
        "attrShowReasonTag": [],
        "attrBusinessPointTag": [],
        "attrWordContainTag": [],
        "showWordContain": "",
        "showWordNotContain": "",
        "pageNo": 1,  # 由于pageSize已经是1000，所以不需要再进行分页查询
        "pageSize": 1000,
        "orderBy": "",
        "order": "",
        "forceReload": True
    }
    form_data = {
        'params': json.dumps(params),
        'path': 'jupiter/GET/kr/word',
        'userid': uconfig['userid'],
        'token': uconfig['token'],
        'eventId': uconfig['eventId'],
        'reqid': uconfig['reqid']
    }

    try:
        resp = requests.post(query, headers=headers, data=form_data, timeout=10)

    except requests.exceptions.RequestException:
        resultitem = {}
        err = "请求了那么多次，百度还是没给返回正确的信息！"
        if retry > 0:
            return get_result_data(key, uconfig, cookie, retry - 1)
    else:
        resp.encoding = 'utf-8'
        try:
            resultitem = resp.json()
        except ValueError:
            resultitem = {}
            err = "获取不到json数据，可能是被封了吧，谁知道呢？"
        else:
            err = None
    return resultitem

def parse_data(datas):
    """用于解析获取回来的json数据
    :param datas: json格式的数据
    :return: 返回关键词列表以及错误信息
    """
    try:
        resultitem = datas['data']['group'][0]['resultitem']
    except (KeyError, ValueError, TypeError):
        kws = []
        err = '获取不到关键词数据'
    else:
        kws = ['{}#{}#{}'.format(item['word'].encode('utf-8'), item['pv'],item['kwc']) for item in resultitem]
        err = None
    return kws
#if __name__ == '__main__':
 #   word  = requests.get("http://127.0.0.1:47576/getwords/%E5%BB%BA%E8%AE%BE/123456")
word = u"seo"

#     sfile = open('resultkeys.txt', 'w')  # 结果保存文件
#     faileds = open('faileds.txt', 'w')  # 查询失败保存文件
#     checkwords = [word.strip() for word in open('checkwords.txt')]  # 要查询的关键词列表
# cookies = open(r'E:\python\bd\cookie.txt').read().strip()  # cookie文件, 里面只放一条可用的cookie即可
#     # 用户配置信息，请自行登录百度凤巢后台通过抓包获取 (以下只是虚拟数据不能直接使用)
config = {
        'userid': 10269030,
        'token': '26c1bf124736361bd2848fb7d1b42df1b1a4ba1dec418b2a5407b5280dfb5560b8bb863079ad3feeecc7de84',
        'eventId': '4b534c46-0482-4882-e43c-150658311652',
        'reqid': '4b534c46-0482-4882-e43c-150658311652'
    }
#     for word in checkwords:
#         print '正在查询:', word
#         print '-' * 50
#    dataresult, error = get_result_data(word, config, cookies)
#         if error:
#             print word, error
#             faileds.write('%s\n' % word)
#             faileds.flush()
#             continue
 #   keywordlist, error = parse_data(dataresult)
#         if error:
#             print word, error
#             faileds.write('%s\n' % word)
#             faileds.flush()
#             continue
  #  for kw in keywordlist:
        # sfile.write("%s\n" % kw)
        # sfile.flush()
    #    print kw
   # print '=' * 50
    #time.sleep(2)  # 每个词的查询间隔时间为2秒，如果不怕被封，可以直接去掉
#     sfile.close()
#     faileds.close()
#     print "所有关键词查询完毕"