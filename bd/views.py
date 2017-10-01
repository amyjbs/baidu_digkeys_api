# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render,HttpResponse,Http404
from bd import baidu
import time
import json,hashlib
# Create your views here.
def getwords(request):

    config = {
    'userid': 10269030,
    'token': '960070297400a1eebffc64b28c107d7f97f752c9e0c54c8fb0d33cbdbb53ae85a5bf6ad354ab39cf7ed4028a',
    'eventId': '4b534c46-636d-4201-a8db-150667462800',
    'reqid': '4b534c46-636d-4201-a8db-150667462800'
    }
    global faileds
    global sfile
    cookies = open("../cookie.txt").read().strip()
    #cookies = "FC-FE-TERMINUS=fc_terminus_user; FC-FE-EDEN=fc_eden_user; BAIDUID=2234CAF82E111AF1B70D3536D9035E47:FG=1; BIDUPSID=2234CAF82E111AF1B70D3536D9035E47; PSTM=1497847550; __cfduid=d7c41dacbc56578ce5b41e3680c637cd41497849355; BDUSS=jJwZ2pxYW5TdWt6YnZ4WnlQN004QXpBNVdIZ2kwNndWUjdTZHhHeWJoaElRZDlaTVFBQUFBJCQAAAAAAAAAAAEAAABAEIYlsrvE3ERPVkUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEi0t1lItLdZQ; __cas__st__3=26c1bf124736361bd2848fb7d1b42df1b1a4ba1dec418b2a5407b5280dfb5560b8bb863079ad3feeecc7de84; __cas__id__3=10269030; __cas__rn__=256583554; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; PSINO=7; H_PS_PSSID=1469_21122_24329_20718; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; SFSSID=ad7c7eb76940d49d2b8a70a0615ca5b6; SIGNIN_UC=70a2711cf1d3d9b1a82d2f87d633bd8a02566043099; uc_login_unique=0e69269627d22a4c77a61e60372a1cca; uc_recom_mark=cmVjb21tYXJrXzEwMjY5MDMw; SAMPLING_USER_ID=10269030"

    token = request.POST.get("token")
    word = request.POST.get("wd")
    m2 = hashlib.md5()
    m2.update("xinmima")
    tokens = m2.hexdigest()
    if token == tokens:
        try:
            dataresult = baidu.get_result_data(word,config,cookies)
            keywordlist = baidu.parse_data(dataresult)
            # for kw in keywordlist:
            #     # result = " ".join(kw)
            #     print kw
            print '=' * 50
            time.sleep(2)  # 每个词的查询间隔时间为2秒，如果不怕被封，可以直接去掉
        except BaseException,e:
            print e
            c = "请求错误"
            return Http404
        # global  words
        # global index
        result=[]
        for kw in keywordlist:
            # words.append(str(kw.split()[0]))
            # index.append(kw.split()[1])
            ws = kw.split("#")[0]
            pv = kw.split("#")[1]
            ops = kw.split("#")[2]
            result_list = [ws,pv,ops]
            result.append(result_list)



        # result = "<br/>".join(keywordlist)

        result[0]="success:200"
        re = json.dumps(result)
        # s =json.loads(re)

        return HttpResponse(re)
    else:
        errors = "非法请求"
        return Http404

