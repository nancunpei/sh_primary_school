import requests
import time
import os
import sys
c = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(c)
try:
    from utils.utils import json2jsonl
except:
    raise


def query_location_tencent(tier, address, district, queue, s=None, reliable=True):
    # 需要开启IP白名单
    url = 'https://apis.map.qq.com/ws/geocoder/v1/'
    key = os.getenv('WX_KEY')
    region = '上海'
    if s:
        s.acquire()
    r = requests.get(
        url, params={'key': key, 'region': region, 'address': address}).json()
    print(r)
    obj = {
        "lat": 0,
        "lon": 0,
        "address": "",
        "tier": ""
    }
    if (r.get('status') == 0 and r.get('result').get('reliability') >= 7 and r.get('result').get('level') >= 9) or (r.get('status') == 0 and not reliable):
        obj['address'] = str(r.get('result').get('title'))
        obj['lat'] = float(r.get('result').get('location').get('lat'))
        obj['lon'] = float(r.get('result').get('location').get('lng'))
        obj['tier'] = tier
        obj['district'] = district
        queue.put(obj)
    elif r.get('status') == 120:  # 请求上限
        print(r)
        time.sleep(0.5)
        query_location_tencent(tier, address, queue, s)
    else:
        print('invalid input', address)
        pass  # todo deal with suspicious address
    if s:
        s.release()


if __name__ == '__main__':
    districts = [
        "静安区",
        "虹口区",
        "崇明区",
        "浦东新区",
        "长宁区",
        "徐汇区",
        "普陀区",
        "奉贤区",
        "金山区",
        "杨浦区",
        "宝山区",
        "嘉定区",
        "青浦区",
        "松江区",
        "闵行区",
        "黄浦区"
    ]
    from queue import Queue
    q = Queue()
    for d in districts:
        query_location_tencent('', '上海市'+d, d,  q, reliable=False)
        time.sleep(0.5)
    data = [q.get() for _ in districts]
    [d.__delitem__('tier') for d in data]
    print(data)
    json2jsonl(data, 'data/district.json')
