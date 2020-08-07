# -*- coding:utf-8 -*-
from urllib.request import urlopen
from urllib.parse import quote
import json
import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default = "firefox"

POOL_SIZE = 512

address_list = []
lat_list = []
lon_list = []


def get_location(address):
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


def draw_location():
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


if __name__ == '__main__':
    with open('data.json') as f:
        sh_address = json.load(f).get('data')

    addresses = []
    for item in sh_address:
        tierA = item.get('tierA').map(lambda x: '上海市' + x if not x.startswith('上海') else x)
        tierB = item.get('tierB').map(lambda x: '上海市' + x if not x.startswith('上海') else x)
        tierC = item.get('tierC').map(lambda x: '上海市' + x if not x.startswith('上海') else x)
        addresses.extend(tierA).extend(tierB).extend(tierC)
    print(addresses)
    for i in addresses:
        get_location(i)
    # # t1 = time.time()
    # pool = threadpool.ThreadPool(POOL_SIZE)
    fig = draw_location()
    fig.show()
    # my_requests = threadpool.makeRequests(get_location, addresses)
    # [pool.putRequest(req) for req in my_requests]
    # pool.wait()
    # pool.dismissWorkers(POOL_SIZE, do_join=True)  # 完成后退出
    # t2 = time.time()
    # print(t2-t1)

