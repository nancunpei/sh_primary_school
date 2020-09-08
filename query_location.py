# -*- coding:utf-8 -*-
from urllib.request import urlopen
from urllib.parse import quote
import json
import plotly.graph_objects as go
import plotly.io as pio
import threading
import pandas as pd
pio.renderers.default = "firefox"


POOL_SIZE = 100

address_list = []
lat_list = []
lon_list = []
tier_list = []
LOCATION_CSV = 'location.csv'


def get_location(tier, address):
    url = 'http://api.map.baidu.com/geocoding/v3/?address='
    output = 'json'
    ak = 'FAjgfSoSquGTrL5cedE50HxhTl7EUqN7'  # 需填入自己申请应用后生成的ak
    add = quote(address)
    url2 = url + add + '&output=' + output + "&ak=" + ak
    req = urlopen(url2)
    res = req.read().decode()
    temp = json.loads(res)
    if temp.get('result'):
        lon = float(temp['result']['location']['lng'])  # 经度 Longitude  简写lon
        lat = float(temp['result']['location']['lat'])  # 纬度 Latitude   简写Lat
    else:
        lon = 0
        lat = 0
    address_list.append(address)
    lat_list.append(lat)
    lon_list.append(lon)
    tier_list.append(tier)


def draw_location():
    df = pd.read_csv(LOCATION_CSV, delim_whitespace=True)
    address_list = df['address'].to_list()
    lat_list = df['lat'].to_list()
    lon_list = df['lon'].to_list()
    tier_list = df['tier'].to_list()

    mapbox_access_token = 'pk.eyJ1Ijoia29wZWkiLCJhIjoiY2tkaDFwOTdlMXdobTJwbXBhd2tlYzYyNiJ9.dwMoIYpHrHgrGTCSrGnHSA'
    fig = go.Figure(go.Scattermapbox(
        lat=lat_list,
        lon=lon_list,
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=14
        ),
        text=address_list
    ))

    fig.update_layout(
        hovermode='closest',
        mapbox=dict(
            accesstoken=mapbox_access_token,
            bearing=0,
            center=go.layout.mapbox.Center(
                lat=31,
                lon=121
            ),
            pitch=0,
            zoom=20
        )
    )

    return fig


def persist_local_csv():
    header = "address lat lon tier"
    with open(LOCATION_CSV, 'w') as f:
        f.write(header+'\n')
        for add, lat, lon, tier in zip(address_list, lat_list, lon_list, tier_list):
            f.write(' '.join([add, str(lat), str(lon), tier, '\n']))


def local_csv_to_json():
    df = pd.read_csv(LOCATION_CSV, delim_whitespace=True)
    df.to_json('location.json', orient='records', force_ascii=False)


def query_location_thread(all_addresses):
    threads = []
    for (tier, address) in all_addresses:
        t = threading.Thread(target=get_location, args=(tier, address))
        t.start()
        threads.append(t)
    [t.join() for t in threads]
    persist_local_csv()
    local_csv_to_json()


def get_boundary():
    url = 'http://api.map.baidu.com/place/v2/search?region=北京&output=json&ak='

with open('data.json') as f:
    sh_address = json.load(f).get('data')

addresses_tierA = []
addresses_tierB = []
addresses_tierC = []
for item in sh_address:
    for tier in ['tierA', 'tierB', 'tierC']:
        l = list(map(lambda x: '上海市' + x if not x.startswith('上海') else x, item.get(tier)))
        if tier == 'tierA':
            addresses_tierA.extend(l)
        elif tier == 'tierB':
            addresses_tierB.extend(l)
        else:
            addresses_tierC.extend(l)

addresses_tierA = [('tierA', i) for i in addresses_tierA]
addresses_tierB = [('tierB', i) for i in addresses_tierB]
addresses_tierC = [('tierC', i) for i in addresses_tierC]
tiered_list = addresses_tierA + addresses_tierB + addresses_tierC
query_location_thread(tiered_list)


# fig = draw_location()
# fig.show()



