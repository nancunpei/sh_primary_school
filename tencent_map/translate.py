import json

import requests
from config.config import WX_KEY


SOGOU_TYPE = 2
BAIDU_TYPE = 3
DEFAULT_TYPE = 5 #google/amap
MAPBAR_TYPE = 4
GPS_TYPE = 1


def translate_from_others(locations, t=BAIDU_TYPE):
    url = 'https://apis.map.qq.com/ws/coord/v1/translate'
    key = WX_KEY
    with open('location.json') as f:
        data = json.load(f)
        print(data)
    for index, l in enumerate(locations):
        r = requests.get(url, params={'locations': l, 'type': t, 'key': key}).json()
        print(r)
        data[index]['lon'] = r.get('locations')[0].get('lng')
        data[index]['lat'] = r.get('locations')[0].get('lat')

    with open('location_wx.json', 'w') as f:
        json.dump(data, f, ensure_ascii=False)


if __name__ == '__main__':
    r = translate_from_others('31.245544889075482,121.56714296727411')
    print(r)

