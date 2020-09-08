var districts = [
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
    "闵行区"
]
function generate(array, callback) {
    // 递归获取boundary数据
    var value = array.pop(0);
    if (value === undefined) {
        // 递归结束
        callback(initGeojson, mapCenter);
        return
    }
    bdary.get(value, function (rs) { //获取行政区域
        var count = rs.boundaries.length; //有多少个地理区间
        var pgType = 'Polygon';
        if (count > 1) {
            pgType = 'MultiPolygon';
        }
        var pgs = {
            type: 'Feature',
            properties: {
                name: value
            },
            geometry: {
                type: pgType,
                coordinates: []
            }
        };
        for (var i = 0; i < count; i++) {
            var bds = rs.boundaries[i];
            //建立多边形覆盖物
            var polygon = new BMap.Polygon(bds, {
                strokeWeight: 2,
                strokeOpacity: 1,
                StrokeStyle: "solid",
                strokeColor: "#9730f7",
                fillOpacity: 0.01
            });
            map.addOverlay(polygon); //添加覆盖物
            //填充pg
            var bdsArray = bds.split(';');
            var line = [];
            $.each(bdsArray, function (idx, point) {
                var p = point.split(',');
                var x = $.trim(p[0]), y = $.trim(p[1]);
                line.push([y, x])
            });
            var pg = [line]
            if (pgType === 'MultiPolygon') {
                pgs.geometry.coordinates.push(pg)
            } else {
                pgs.geometry.coordinates = pg
            }
        }
        initGeojson.features.push(pgs);
        generate(array, callback);
    });
}

function prepareDownload(data, name) {
    var text = JSON.stringify(data);
    var type = 'text/plain';
    var downbtn = document.getElementById("download");
    var file = new Blob([text], {type: type});
    downbtn.href = URL.createObjectURL(file);
    downbtn.download = name + '.json';
    downbtn.style.visibility = 'visible';
}

generate(districts, prepareDownload);
