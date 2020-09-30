import os
import time

import requests


def query_location_tencent(tier, address, district, queue, s=None):
    # 需要开启IP白名单
    url = 'https://apis.map.qq.com/ws/geocoder/v1/'
    key = os.getenv('WX_KEY')
    region = '上海'
    s.acquire()
    r = requests.get(
        url, params={'key': key, 'region': region, 'address': address}).json()
    obj = {
        "lat": 0,
        "lon": 0,
        "address": "",
        "tier": ""
    }
    if r.get('status') == 0 and r.get('result').get('reliability') >= 7 and r.get('result').get('level') >= 9:
        obj['address'] = str(r.get('result').get('title'))
        obj['lat'] = float(r.get('result').get('location').get('lat'))
        obj['lon'] = float(r.get('result').get('location').get('lng'))
        obj['tier'] = tier
        obj['district'] = district
        queue.put(obj)
    elif r.get('status') == 120:  # 请求上限
        print(r)
        time.sleep(1)
        query_location_tencent(tier, address, queue, s)
    else:
        print('invalid input', address)
        pass  # todo deal with suspicious address

    s.release()


if __name__ == '__main__':
    query_location_tencent('tierA', '上海上师大一附小', '静安区',  [])
