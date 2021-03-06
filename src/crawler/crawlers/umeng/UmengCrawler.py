# -*- coding: UTF-8 -*-
# from selenium import webdriver
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.common.exceptions import WebDriverException
import datetime
import time
import urllib2
import urllib
import re
import json
import cookielib


class UmengCrawler:
    def __init__(self):
        self.host = 'mobile.umeng.com'
        self.username = 'develop@arashivision.com'
        self.password = ')8x3CpA$'
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'
        self.cookie = ''
        self.headers = {}
        self.headers['User-Agent'] = self.user_agent
        self.headers['Host'] = self.host
        self.headers['X-Requested-With'] = 'XMLHttpRequest'
        self.headers['Connection'] = 'keep-alive'
        self.headers['Cache-Control'] = 'max-age=0'
        self.headers['Accept'] = '*/*'
        self.headers['Accept-Language'] = 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'
        self.headers['X-CSRF-Token'] = 'gnRA365zNecgXvbLpUca20a4uSLO40G/gFNp1sCqJZA='
        self.start()

    def start(self):
        request = urllib2.Request('https://i.umeng.com')
        response = urllib2.urlopen(request)
        page = response.read()
        pattern = re.compile("token: '.*'", re.S)
        items = re.findall(pattern, page)
        token = items[0][8:40]
        pattern = re.compile("sessionid: '.*'", re.S)
        items = re.findall(pattern, page)
        sessionid = items[0][12:52]
        date = str(int(time.time()))
        cookie = cookielib.CookieJar()
        handler = urllib2.HTTPCookieProcessor(cookie)
        opener = urllib2.build_opener(handler)

        values = {'token': token, 'username': self.username, 'password': self.password, 'website': 'umengplus',
                  'sig': '', 'sessionid': '', 'app_id': '', 'url': ''}
        headers = {}
        headers['User-Agent'] = self.user_agent
        headers['Host'] = 'i.umeng.com'
        headers['X-Requested-With'] = 'XMLHttpRequest'
        headers['Connection'] = 'keep-alive'
        headers['Referer'] = 'https://i.umeng.com/'
        headers['Accept'] = '*/*'
        headers['Content-Length'] = '141'
        headers['Accept-Language'] = 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'
        headers[
            'Cookie'] = '"_uab_collina=147003374645454333577887; CNZZDATA1258498910=1811473854-1470033345-%7C' + date + '; l=Al5e4Lp4E3ELprr25VQtL1jijv-gjSKb; isg=AsDAv10dgz1iZH8ZBR9Gkm3Jkk61t6QTerYlFDpRHltstWLf4lv0o0RPu4eZ; cna=m6slEI92cRUCATo8eHdZ2zu1; pgv_pvi=9910472704; _ga=GA1.2.425559374.1470034774; um_lang=zh; cn_1259864772_dplus=%7B%22distinct_id%22%3A%20%221564f05caab5bc-0dfe620d9c6d14-13666c4a-1fa400-1564f05caac623%22%2C%22%E6%98%AF%E5%90%A6%E7%99%BB%E5%BD%95%22%3A%20false%2C%22%24_sessionid%22%3A%200%2C%22%24_sessionTime%22%3A%201471500672%2C%22%24dp%22%3A%200%2C%22%24_sessionPVTime%22%3A%201471500672%2C%22initial_view_time%22%3A%20%221470385261%22%2C%22initial_referrer%22%3A%20%22http%3A%2F%2Fmobile.umeng.com%2Fapps%2F7e71006215a55f0ed1313175%2Freports%2Frealtime_summary%22%2C%22initial_referrer_domain%22%3A%20%22mobile.umeng.com%22%2C%22%24recent_outside_referrer%22%3A%20%22%24direct%22%7D; UMPLUSCENTER=' + sessionid + '; __ufrom=https://i.umeng.com/user/products; pgv_si=s1276146688; cn_a61627694930aa9c80cf_dplus=%7B%22distinct_id%22%3A%20%2215644d6da2f6c4-0ab3e3fe06fb2c-13666c4a-1fa400-15644d6da30649%22%2C%22%24_sessionid%22%3A%201%2C%22%24_sessionTime%22%3A%201472107624%2C%22%24dp%22%3A%200%2C%22%24_sessionPVTime%22%3A%201472107624%2C%22initial_view_time%22%3A%20%221470033345%22%2C%22initial_referrer%22%3A%20%22%24direct%22%2C%22initial_referrer_domain%22%3A%20%22%24direct%22%2C%22%24recent_outside_referrer%22%3A%20%22%24direct%22%2C%22%E7%94%A8%E6%88%B7%E5%90%8D%22%3A%20%22develop%40arashivision.com%22%7D; umengplus_name=develop%40arashivision.com; umplusuuid=47df653d80020a28ea83af935ad8d6e0; umplusappid=umcenter"'
        data = urllib.urlencode(values)
        request = urllib2.Request(url='https://i.umeng.com/login/ajax_do', data=data, headers=headers)
        result = opener.open(request)
        print result.read()
        for c in cookie:
            self.cookie = self.cookie + c.name + '=' + c.value + ';'
        self.headers['Cookie'] = self.cookie

    def getNewUser(self, start_date, end_date):
        self.headers['Referer'] = 'http://mobile.umeng.com/apps/cf41008f4de85e761c647675/reports/installation'
        request = urllib2.Request(
            'http://mobile.umeng.com/apps/cf41008f4de85e761c647675/reports/load_table_data?page=1&per_page=99999&start_date=' + start_date + '&end_date=' + end_date + '&versions[]=&channels[]=&segments[]=&time_unit=daily&stats=installations',
            headers=self.headers)
        try:
            response = urllib2.urlopen(request)
            jsonData = response.read()
            result = json.loads(jsonData, encoding="utf-8")
            # print result['stats']
            return result['stats']
        except urllib2.URLError, e:
            if hasattr(e, "code"):
                print e.code
            if hasattr(e, "reason"):
                print e.reason

    def getActiveUser(self, start_date, end_date):
        self.headers['Referer'] = 'http://mobile.umeng.com/apps/cf41008f4de85e761c647675/reports/active_user'
        request = urllib2.Request(
            'http://mobile.umeng.com/apps/cf41008f4de85e761c647675/reports/load_table_data?page=1&per_page=99999&start_date=' + start_date + '&end_date=' + end_date + '&versions[]=&channels[]=&segments[]=&time_unit=daily&stats=active_users',
            headers=self.headers)
        try:
            response = urllib2.urlopen(request)
            jsonData = response.read()
            result = json.loads(jsonData, encoding="utf-8")
            # print result['stats']
            return result['stats']
        except urllib2.URLError, e:
            if hasattr(e, "code"):
                print e.code
            if hasattr(e, "reason"):
                print e.reason

    def getDuration(self, date):
        self.headers['Referer'] = 'http://mobile.umeng.com/apps/cf41008f4de85e761c647675/reports/duration'
        request = urllib2.Request(
            'http://mobile.umeng.com/apps/cf41008f4de85e761c647675/reports/load_chart_data?start_date=' + date + '&end_date=' + date + '&versions[]=&channels[]=&segments[]=&time_unit=daily&stats=duration&stat_type=daily',
            headers=self.headers)
        try:
            response = urllib2.urlopen(request)
            jsonData = response.read()
            result = json.loads(jsonData, encoding="utf-8")
            # print result['summary']['value']
            return result['summary']['value']
        except urllib2.URLError, e:
            if hasattr(e, "code"):
                print e.code
            if hasattr(e, "reason"):
                print e.reason

    def getTotalError(self, start_date, end_date):
        self.headers['Referer'] = 'http://mobile.umeng.com/apps/cf41008f4de85e761c647675/error_types/trend'
        request = urllib2.Request(
            'http://mobile.umeng.com/apps/cf41008f4de85e761c647675/reports/load_chart_data?start_date=' + start_date + '&end_date=' + end_date + '&stats=error_count',
            headers=self.headers)
        result = []
        try:
            response = urllib2.urlopen(request)
            jsonData = response.read()
            res = json.loads(jsonData, encoding="utf-8")
            data = res['stats'][0]['data']
            dates = res['dates']
            for index in range(len(dates)):
                temp = {'date': dates[index], 'total_error': data[index]}
                result.append(temp)
        except urllib2.URLError, e:
            if hasattr(e, "code"):
                print e.code
            if hasattr(e, "reason"):
                print e.reason
        jsonResult = json.dumps(result)
        return jsonResult


    def getErrorRate(self, start_date, end_date):
        self.headers['Referer'] = 'http://mobile.umeng.com/apps/cf41008f4de85e761c647675/reports/trend_summary'
        request = urllib2.Request(
            'http://mobile.umeng.com/apps/cf41008f4de85e761c647675/reports/load_chart_data?start_date=' + start_date + '&end_date=' + end_date + '&stats=trend_error_rate',
            headers=self.headers)
        result = []
        try:
            response = urllib2.urlopen(request)
            jsonData = response.read()
            res = json.loads(jsonData, encoding="utf-8")
            data = res['stats'][0]['data']
            dates = res['dates']
            for index in range(len(dates)):
                temp = {'date': dates[index], 'error_rate': data[index]}
                result.append(temp)
        except urllib2.URLError, e:
            if hasattr(e, "code"):
                print e.code
            if hasattr(e, "reason"):
                print e.reason
        jsonResult = json.dumps(result)
        return jsonResult


    def getErrorDetail(self, start_date, end_date):
        # start_date 必须在今天的前15天之后
        self.headers['Referer'] = 'http://mobile.umeng.com/apps/cf41008f4de85e761c647675/error_types'
        request = urllib2.Request(
            'http://mobile.umeng.com/apps/cf41008f4de85e761c647675/error_types/search?start_date=' + start_date + '&end_date=' + end_date + '&versions[]=1.2.0&versions[]=1.2.1&versions[]=1.1.0&message_type=legit&per_page=99999&page=0&order_by=desc_error_count',
            headers=self.headers)
        try:
            response = urllib2.urlopen(request)
            jsonData = response.read()
            result = json.loads(jsonData, encoding="utf-8")
            return result['result']
        except urllib2.URLError, e:
            if hasattr(e, "code"):
                print e.code
            if hasattr(e, "reason"):
                print e.reason

    def getUserCityDistribution(self, start_date, end_date):
        self.headers['Referer'] = 'http://mobile.umeng.com/apps/cf41008f4de85e761c647675/reports/location?which=cities'
        request = urllib2.Request(
            'http://mobile.umeng.com/apps/cf41008f4de85e761c647675/reports/load_table_data?page=1&per_page=99999&start_date=' + start_date + '&end_date=' + end_date + '&versions[]=&channels[]=&segments[]=&time_unit=daily&stats=location_cities',
            headers=self.headers)
        try:
            response = urllib2.urlopen(request)
            jsonData = response.read()
            result = json.loads(jsonData, encoding="utf-8")
            return result['stats']
        except urllib2.URLError, e:
            if hasattr(e, "code"):
                print e.code
            if hasattr(e, "reason"):
                print e.reason
        except KeyError:
            return {}

    def getUserCountryDistribution(self, start_date, end_date):
        self.headers[
            'Referer'] = 'http://mobile.umeng.com/apps/cf41008f4de85e761c647675/reports/location?which=countries'
        request = urllib2.Request(
            'http://mobile.umeng.com/apps/cf41008f4de85e761c647675/reports/load_table_data?page=1&per_page=99999&start_date=' + start_date + '&end_date=' + end_date + '&versions[]=&channels[]=&segments[]=&time_unit=daily&stats=location_countries',
            headers=self.headers)
        try:
            response = urllib2.urlopen(request)
            jsonData = response.read()
            result = json.loads(jsonData, encoding="utf-8")
            res = result['result']
            return result['stats']
        except urllib2.URLError, e:
            if hasattr(e, "code"):
                print e.code
            if hasattr(e, "reason"):
                print e.reason
        except KeyError:
            return {}

    def getUserDistribution(self, start_date, end_date):
        start = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        end = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
        result = []
        for i in range((end - start).days + 1):
            date = (end - datetime.timedelta(days=i)).strftime('%Y-%m-%d')
            city = self.getUserCityDistribution(date, date)
            for item in city:
                is_native = 1
                if item['date'] == '香港' or item['date'] == '台湾' or item['date'] == '澳门':
                    is_native = 0
                temp = {'date': date, 'location': item['date'], 'active_user': item['active_data'],
                        'active_rate': item['active_rate'], 'new_user': item['install_data'],
                        'new_rate': item['install_rate'], 'launch_data': item['launch_data'],
                        'launch_rate': item['launch_rate'], 'is_native': is_native}
                result.append(temp)
            country = self.getUserCountryDistribution(date, date)
            for item in country:
                temp = {'date': date, 'location': item['date'], 'active_user': item['active_data'],
                        'active_rate': item['active_rate'], 'new_user': item['install_data'],
                        'new_rate': item['install_rate'], 'launch_data': item['launch_data'],
                        'launch_rate': item['launch_rate'], 'is_native': 0}
                result.append(temp)
        jsonResult = json.dumps(result)
        return jsonResult

    def getUseCondition(self, start_date, end_date):
        result = []
        newUser = self.getNewUser(start_date, end_date)
        activeUser = self.getActiveUser(start_date, end_date)
        start = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        end = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
        for i in range((end - start).days + 1):
            date = (end - datetime.timedelta(days=i)).strftime('%Y-%m-%d')
            durationStr = self.getDuration(date)
            temp = durationStr.split(':')
            duration = int(temp[0]) * 3600 + int(temp[1]) * 60 + int(temp[2])
            print date, newUser[i]['data'], activeUser[i]['data'], duration
            temp = {'date': date, 'new_user': newUser[i]['data'], 'active_user': activeUser[i]['data'],
                    'duration': duration}
            result.append(temp)
        jsonResult = json.dumps(result)
        return jsonResult


    def getEvent(self, start_date, end_date, event_group_id, version):
        self.headers['Referer'] = 'http://mobile.umeng.com/apps/cf41008f4de85e761c647675/events/' + event_group_id + '?version='
        request = urllib2.Request(
            'http://mobile.umeng.com/apps/cf41008f4de85e761c647675/events/load_table_data?page=1&per_page=99999&start_date=' + start_date + '&end_date=' + end_date + '&versions[]=' + version + '&channels[]=&stats=event_group_trend&event_group_id=' + event_group_id,
            headers=self.headers
        )
        try:
            response = urllib2.urlopen(request)
            jsonData = response.read()
            result = json.loads(jsonData, encoding="utf-8")
            return result['stats']
        except urllib2.URLError, e:
            if hasattr(e, "code"):
                print e.code
            if hasattr(e, "reason"):
                print e.reason


    def getVersions(self):
        self.headers['Referer'] = 'http://mobile.umeng.com/apps/cf41008f4de85e761c647675/events/dashboard'
        request = urllib2.Request(
            'http://mobile.umeng.com/apps/cf41008f4de85e761c647675/load_versions?show_all=true',
            headers=self.headers
        )
        try:
            response = urllib2.urlopen(request)
            jsonData = response.read()
            result = json.loads(jsonData, encoding="utf-8")
            datas = result['datas']
            versions = []
            for data in datas:
                versions.append(data['name'])
            return versions
        except urllib2.URLError, e:
            if hasattr(e, "code"):
                print e.code
            if hasattr(e, "reason"):
                print e.reason


    def getShareChannel(self, start_date, end_date):
        event_group_ids = {
            '微信_img': '57afe74767e58ea4ca000428',
            'Facebook_img': '57afe75ce0f55a34db00349c',
            'Whatsapp_img': '57afe7a267e58edf73002e91',
            'Facebook_video': '57afe6ce67e58eb85a0046e5',
            '链接_video': '5858e1fdf5ade402780010ac',
            '微信_video': '57afe6bee0f55a480400445a',
            'Line_img': '57afe7bce0f55ac27900447b',
            'Whatsapp_video': '57afe71b67e58e317b003814',
            'Moment_img': '57afe78567e58e3c1f001b74',
            'Instagram_video': '5858e1f17666135f19000550',
            '链接_img': '5858e214f5ade44ac9000fce',
            'Youtube_video': '57afe6ed67e58e84230001c1',
            'Messenger_img': '57afe7af67e58e7837001ac7',
            'Line_video': '57afe73767e58e6bc80006b2',
            'Instagram_img': '5858e209c895765ac5001b99',
            '朋友圈_video': '57afe70067e58e86c5003cfe',
            'Messenger_video': '57afe728e0f55a7b52002ba4',
            'QQ_img': '57afed8667e58e42aa0005da',
            '微博_video': '57afe70e67e58e5f2f005a1e',
            'QQ_video': '57afed9f67e58eb85a004bfd',
            'Twitter_img': '57afe76b67e58ef70b003503',
            '微博_img': '57afe794e0f55ac8e3000e81',
            'Qzone_video': '57afedaa67e58e6bc8000c4d',
            'Twitter_video': '57afe6dd67e58e86ad000af7',
            'Qzone_img': '57afed9267e58e4759002409'
        }
        versions = self.getVersions()
        result = []
        for version in versions:
            if version < '1.3.0':
                continue
            for index in event_group_ids:
                event_group_id = event_group_ids[index]
                data = self.getEvent(start_date, end_date, event_group_id, version)
                print data
                temps = index.split('_')
                temp = {
                    'version': version,
                    'event_group_id': event_group_id,
                    'channel': temps[0],
                    'type': temps[1],
                    'data': data
                }
                result.append(temp)
        jsonResult = json.dumps(result)
        return jsonResult


    def getShareCount(self, start_date, end_date):
        event_group_ids = {
            'video_success': '576ba13767e58eb24f001ee5',
            'video_try': '576ca33267e58e9c380026a4',
            'img_try': '576ca36067e58ed3450030a8',
            'img_success': '576ba15a67e58e15b2001435'
        }
        versions = self.getVersions()
        result = []
        for version in versions:
            if version < '1.6.0':
                continue
            for index in event_group_ids:
                event_group_id = event_group_ids[index]
                data = self.getEvent(start_date, end_date, event_group_id, version)
                temps = index.split('_')
                temp = {
                    'version': version,
                    'event_group_id': event_group_id,
                    'data': data,
                    'type': temps[0],
                    'flag': temps[1]
                }
                result.append(temp)
        jsonResult = json.dumps(result)
        return jsonResult



if __name__ == "__main__":
    crawler = UmengCrawler()
    print crawler.getUseCondition('2016-08-08', '2016-08-12')
