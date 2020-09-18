import os
from urllib.request import urlopen
from urllib.parse import quote

import json


def get_location(tier, address, queue, s):
    url = 'http://api.map.baidu.com/geocoding/v3/?address='
    output = 'json'
    ak = os.getenv('BAIDU_AK', 'FAjgfSoSquGTrL5cedE50HxhTl7EUqN7')  # 需填入自己申请应用后生成的ak
    add = quote(address)
    url2 = url + add + '&output=' + output + "&ak=" + ak
    with s:
        req = urlopen(url2)
        res = req.read().decode()
        temp = json.loads(res)
        if temp.get('result'):
            lon = float(temp['result']['location']['lng'])  # 经度 Longitude  简写lon
            lat = float(temp['result']['location']['lat'])  # 纬度 Latitude   简写Lat
        else:
            lon = 0
            lat = 0

        obj = dict()
        obj['address'] = address
        obj['lat'] = lat
        obj['lon'] = lon
        obj['tier'] = tier
        queue.put(obj)
