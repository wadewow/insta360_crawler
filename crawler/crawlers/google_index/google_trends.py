# -*- coding: UTF-8 -*-
import sys
import json
import time
import urllib
import requests
import ssl
import datetime
import calendar
from functools import wraps

reload(sys)
sys.setdefaultencoding("utf-8")

def google_index():
    ssl.wrap_socket = sslwrap(ssl.wrap_socket)
    tasks = ['insta360', 'gear 360', 'theta s', 'okaa', 'eyesir', 'ZMER', '全景相机']
    result = []
    for task in tasks:
        result.extend(get_google_trend(task))
    jsonResult = json.dumps(result)
    print jsonResult
    return jsonResult


def get_google_trend(key):
    headers = {}
    headers['Host'] = 'www.google.com'
    headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0'
    headers['Referfer'] = 'https://www.google.com/trends/explore?date=today%201-m&q=' + urllib.quote(key)
    headers['Cookie'] = '__utma=173272373.1277331075.1476358092.1476358092.1476415913.2; __utmz=173272373.1476358092.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmb=173272373.2.10.1476415913; __utmc=173272373; __utmt=1; NID=84=lT0Y5iF9rOA6QJn8KF04H5f1N7J7bMkQbUSiA9eJnY3-mBpf6OOz1dBQWJBi9BHnXzb3OmQW0d2DslexTFNU5Mr1dTjfEM2CD22BB5yAM44IL_vi9-BWG1C6QjL6XRFk'
    headers['Connection'] = 'keep-alive'
    headers['Accept'] = 'application/json, text/plain, */*'
    headers['Accept-Language'] = 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'
    headers['Accept-Encoding'] = 'gzip, deflate, br'

    now = datetime.datetime.now()
    month = (now.month + 10) % 12 + 1
    year = now.year - month / 12
    day = min(now.day, calendar.monthrange(year, month)[1])
    before = now.replace(year=year, month=month, day=day)
    start_date = before.strftime('%Y-%m-%d')
    end_date = now.strftime('%Y-%m-%d')
    req = {}
    req['time'] = start_date + "+" + end_date
    req['resolution'] = "DAY"
    req['locale'] = "zh-CN"
    req['comparisonItem'] = [{"geo": {}, "complexKeywordsRestriction": {"keyword": [{"type": "BROAD", "value": urllib.quote(key).replace(' ','+')}]}}]
    req['requestOptions'] = {"property":"","backend":"IZG","category":0}
    token = {}
    token['insta360'] = 'APP6_UEAAAAAWAGjNJGHS4AQNqSxW_aEzJflcYdmU8Cf'
    token['gear 360'] = 'APP6_UEAAAAAWAH6C5JADso2REBkg4KxsFb-mj3ykgbL'
    token['theta s'] = 'APP6_UEAAAAAWAH8N9ktotf5V72A1x9Q3jUKnOPfs5ti'
    token['okaa'] = 'APP6_UEAAAAAWAH8pNtsCvmezK6r_tb72fAvE2m5yy27'
    token['eyesir'] = 'APP6_UEAAAAAWAH87KAQbNLdZIniPEbcaokRE7nNiVWu'
    token['ZMER'] = 'APP6_UEAAAAAWAH9GuVVoPraOWcToR83HBsnZA932bMk'
    token['全景相机'] = 'APP6_UEAAAAAWAH9YSWCjXzD3WWRMkchV2LECmi7lXHC'
    value = {}
    value['hl'] = 'zh-CN'
    value['tz'] = '-480'
    value['req'] = str(req).replace(' ','')
    value['token'] = token[key]
    url = 'https://www.google.com/trends/api/widgetdata/multiline?'
    for index in value:
        url = url + index + '=' + value[index] + '&'
    results = requests.get(url, headers=headers)
    page = results.content
    print page
    jsonData = page[5:]
    data = json.loads(jsonData, encoding="utf-8")
    items = data['default']['timelineData']
    result = []
    for item in items:
        timestamp = int(item['time'])
        time_temp = time.localtime(timestamp)
        date = time.strftime("%Y-%m-%d", time_temp)
        value = item['value'][0]
        temp = {'key': key, 'date': date, 'google_index': value}
        result.append(temp)
    return result


def sslwrap(func):
    @wraps(func)
    def bar(*args, **kw):
        kw['ssl_version'] = ssl._PROTOCOL_NAMES
        return func(*args, **kw)
    return bar


if __name__ == '__main__':
    google_index()