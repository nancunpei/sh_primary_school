import os

import requests


suspicious_addresses = []
address_list = []
lon_list = []
lat_list = []
tier_list = []


def query_location_tencent(tier, address):
    url = 'https://apis.map.qq.com/ws/geocoder/v1/'
    key = os.getenv('WX_KEY')
    sk = os.getenv('WX_SK', '')
    region = '上海'
    r = requests.get(url, params={'key': key, 'region': region, 'address': address}).json()
    print(r)
    if r.get('status') == 0 and r.get('result').get('reliability') >=7 and r.get('result').get('level') >=9:
        address_list.append(r.get('result').get('title'))
        lat_list.append(r.get('result').get('location').get('lat'))
        lon_list.append(r.get('result').get('location').get('lng'))
        tier_list.append(tier)


if __name__ == '__main__':
    query_location_tencent('tierA', '上海上师大一附小')
    print(address_list)
    print(lon_list)
    print(lat_list)
