# -*- coding:utf-8 -*-
import requests, threading, time, json
from  datetime import datetime


class Comm():
    rcontent = {}
    resp_str = []

    def build_response(self, start, res, tt, ip):
        response_str, context = '', ''
        if res:
            response_str = res.text.replace('null', 'None').replace('false', 'False').replace('true', 'True')
            context = json.dumps(eval(response_str), indent=4, ensure_ascii=False)
        else:
            context = 'ERROR:返回数据为空，接口处理异常！'
        if ip:
            tip = "\r\n" + "=====" * 2 + "请求时间:" + str(start)[:-2] + '=====' + "耗时:" + tt + '=====' * 2 + "\r\n"
            self.resp_str.append(tip + context)
            self.rcontent.update({ip: ''.join(self.resp_str)})
        return response_str

    def api_getdata(self, apiurl, apidata, ck, header, **kwargs):
        #参数ck是cookies，ver=0用request模块，ver=1用urllib2模块
        #session = requests.Session()
        print("post_cookie:%s" % ck)
        start = datetime.now()
        start_timestamp = time.time()
        r = requests.post(apiurl, data=apidata, headers=header, cookies=ck, verify=False)
        seconds = str(round((time.time() - start_timestamp), 4)) + '秒'
        response_str = self.build_response(start, r, seconds, kwargs.get('ip'))
        return [response_str, apiurl]  #return返回的数据

    def build_header(self, host):
        user_Agent = ''
        ContentType = 'application/x-www-form-urlencoded; charset=utf-8'
        if host.split('|')[1] == 'mm':
            user_Agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, ' \
                         'like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
        elif host.split('|')[1] == 'md':
            user_Agent = 'Android APPXIUCHEZAI/1.6.3'
        elif host.split('|')[1] == 'pc' or host.split('|')[1] == 'sp':
            user_Agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                         'Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0'
        elif host.split('|')[1] == 'sa':
            user_Agent = 'ANDROID APPXIUCHEZAISGMW/1.2.7Beta'
        header = {'Host': host.split('//')[1].split('|')[0], 'Connection': 'keep-alive', 'Accept': '*/*',
                  'User-Agent': user_Agent, 'Content-Type': ContentType, 'Accept-Encoding': 'gzip, deflate'}
        print('build_header:%s' % header)
        return header

    def do_test(self, formdata):
        threads = []
        self.resp_str = []
        header = self.build_header(formdata.get('host'))
        if formdata.get('check_login') == False:  #无需登录
            print('no user')
            for i in range(1, formdata.get('thread_num') + 1):
                t = threading.Thread(target=self.api_getdata,
                                     args=(formdata.get('url'), formdata.get('data'), formdata.get('cookies'), header),
                                     kwargs={'ip': formdata.get('ip')})
                t.setDaemon(True)
                threads.append(t)
        else:  #合并cookie，_s_openid+登录后的
            host = formdata.get('host').split('|')[0]
            host_flag = formdata.get('host').split('|')[1]
            pwd, stock = formdata.get('pwd'), ['', '']
            if formdata.get('stock_list'):
                stock = [formdata.get('stock_id'), formdata.get('stock_name')]
            if host_flag[0] == 's':  #sgmw项目
                pwd = formdata.get('password')
            formdata.get('cookies').update(
                self.get_cookies(host_flag, host=host, companycode=formdata.get('company'),
                                 username=formdata.get('username'), password=pwd, stock=stock, header=header))
            # print("cookieOpenId:%s" % formdata.get('cookies'))
            for i in range(1, formdata.get('thread_num') + 1):
                t = threading.Thread(target=self.api_getdata,
                                     args=(formdata.get('url'), formdata.get('data'), formdata.get('cookies'), header),
                                     kwargs={'ip': formdata.get('ip')})
                t.setDaemon(True)
                threads.append(t)

        for t in threads:
            t.start()

        for t in threads:
            t.join()

    def get_cookies(self, site_type, host='', companycode='', username='', password='', header=None, stock=None):
        #site:0M站，1PC站,99SGMW信息采集登录接口
        myCookie = {}
        try:
            url_qsh = host + '/Login/LoginAction.do'
            url_sgmw = host + '/oa-site/login/login.do'
            if site_type == 'mm':  #M站
                data = {'txt_zh': username, 'txt_pwd': password}
                r = requests.post(url_qsh, data, headers=header).text
                myCookie = {"cookie_uuid": eval(r)['data']['cookie_uuid']}
            elif site_type == 'md':  #门店app
                data = {"txt_zh": username, "txt_pwd": password, "stock_id": stock[0], "stock_name": stock[1]}
                r = requests.post(url_qsh, data, headers=self.build_header(host + '|mm')).text
                myCookie = {"cookie_uuid": eval(r)['data']['cookie_uuid']}
                #myCookie = {'cookie_uuid': r.cookies['cookie_uuid'], 'cookie_userInfo': r.cookies['cookie_userInfo']}
            elif site_type == 'pc':
                data = {"login_type": "1", "txt_zh": username, "txt_pwd": password, "stock_id": stock[0],
                        "stock_name": stock[1]}
                r = requests.post(url_qsh, data, headers=header)
                myCookie = {'cookie_uuid': r.cookies['cookie_uuid'], 'cookie_userInfo': r.cookies['cookie_userInfo']}
            elif site_type == 'sa':
                data = {"companyCode": companycode, "account": username, "password": password, "client": "app"}
                r = requests.post(url_sgmw, data, headers=header, verify=False)
                myCookie = {"JSESSIONID": r.cookies['JSESSIONID']}
            elif site_type == 'sp':
                data = {"companyCode": companycode, "account": username, "password": password, "client": "pc"}
                r = requests.post(url_sgmw, data, headers=header, verify=False)
                myCookie = {"JSESSIONID": r.cookies['JSESSIONID']}
            print("myCookie:%s" % myCookie)
            return myCookie
        except BaseException as e:
            print('eeee', e)

    def handle_stock(self, stock_list, stock_id):
        st_list = stock_list.split('\r\n')
        for i in range(st_list.__len__()):
            if st_list[i][0] == stock_id:
                return st_list[i].split('|')[1].strip()

    def str_to_dict0(self, txt):
        '''将类似car_conf_id:574,car_id:44这种str格式转换成Dict格式
        car_id:44,sale_json:[{attr_id:1,attr_name:ccc,attr_value:red,attr_code:1}]'''
        if txt.find('{') == -1:
            txt = '{"' + txt.replace(':', '":"').replace(',', '","') + '"}'
            return txt
        else:
            tt = str(self.str_to_dict1(txt))
            #返回car_id":"44,sale_json":[{attr_id":"1,attr_value":"red,attr_code":"1}]
            tt = '{"' + tt.replace(',', '","').replace('{', '{"').replace('}', '"}') + '}'
            return tt

    def str_to_dict1(self, txt):
        ttt = txt
        count = ttt.count(':')
        ix = 0
        for a in range(count):
            index = ttt.index(':', ix)
            #print index
            ix = index + 2
            if ttt[index + 1:index + 2] == '[':
                ttt = ttt[:index] + ttt[index:].replace(':', '":', 1).replace('[', "'[", 1).replace(']', "]'")
            elif ttt[index + 1:index + 2] == '{':
                ttt = ttt[:index] + ttt[index:].replace(':', '":', 1).replace('{', "'{", 1)
                tttindex = str(ttt).rfind('}')
                ttt = ttt.replace(ttt[tttindex:tttindex + 1], "}'")
            else:
                ttt = ttt[:index] + ttt[index:].replace(':', '":"', 1)
        #ttt = '{"' + ttt.replace(',', '","').replace('{', '{"').replace('}', '"}') + '}'
        ttt = '"' + ttt.replace('{', '{"').replace('}', '"}')
        nn = ttt.count(',')
        ix = 0
        for a in range(nn):
            aindex = ttt.index(',', ix)
            ix = aindex + 2
            if ttt[aindex - 1:aindex] != '}' and ttt[aindex:aindex + 1] != '{':
                ttt = ttt[:aindex] + '","' + ttt[aindex + 1:]
        return ttt

    def str_to_dict2(self, line):
        ix = 0
        nn = line.count(',')
        #print nn
        for a in range(nn):
            aindex = line.index(',', ix)
            ix = aindex + 2
            if line[aindex - 1:aindex] != '}' and line[aindex:aindex + 1] != '{':
                line = line[:aindex] + '","' + line[aindex + 1:]
        return line

    def str_to_dict(self, file_temp):
        l = ''
        for line in file_temp:
            if (line == '\r\n'):
                continue
            elif (line == '\n'):
                continue
            else:
                line = line.strip('\r')
                line = line.strip('\n')
            if line.find('{') == -1:
                line = '"' + line.replace(":", '":"', 1) + '"'
            elif line.find('":') > 0 or line.find("':") > 0:
                line = '"' + line.replace(":", "\":'", 1) + "'"
            else:
                line = self.str_to_dict1(line)
            #返回sale_json":[{attr_id":"1,attr_value":"red,attr_code":"1}]
            #line = '"' + line.replace('{', '{"').replace('}', '"}')
            #line = str_to_dict2(line)
            l = l + ',' + line
        l = '{' + l[1:] + '}'
        return eval(l)

    def str_format(self, t):
        c = t.split('{')
        k = '{'
        n = '\n'
        t = '    '
        j = '{'
        for i in range(1, len(c) - 1):
            j = j + (c[i] + n + t + k + n + t * 2)
        return (j + c[-1])

    def str_to_dictRawline(self, requestData, type='json'):
        try:
            txtlst = []
            r = ''
            if requestData == "" or requestData == None or requestData == {}:
                return {}
            elif requestData[0] == '{' and requestData[-1] == '}':
                return eval(requestData)
            if requestData.find('\r\n') == -1:
                if type == 'json':
                    txtlst = eval(self.str_to_dict0(requestData))
                    return txtlst
                elif type == 'raw':
                    txtlst = requestData.strip().split(',')
            elif requestData.find('\r\n') >= 0:
                if type == 'json':
                    #转换成dict格式
                    fileNameTemp = 'temp.txt'
                    with open(fileNameTemp, 'w') as file_temp:
                        file_temp.write(requestData)
                    with open(fileNameTemp, 'r') as file_temp:
                        temp = self.str_to_dict(file_temp)
                        return temp
                elif type == 'raw':
                    txtlst = requestData.strip().split('\r\n')
            for i in txtlst:
                i = i.replace(':', '=', 1)
                r = r + i + '&'
            r = r[:-1].encode('utf-8')
            return r
        except BaseException as e:
            print(e)
