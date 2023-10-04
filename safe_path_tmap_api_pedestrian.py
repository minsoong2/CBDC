import requests
import folium
from folium import plugins
import pandas as pd
import haversine
import math
from folium.plugins import MarkerCluster


start_lat = 35.22254876728935
start_lng = 128.68869123457196
end_lat = 35.24131123348904
end_lng = 128.69584150197073


m = folium.Map(location=[start_lat, start_lng], zoom_start=15)
folium.Marker([start_lat, start_lng], tooltip='출발지').add_to(m)
folium.Marker([end_lat, end_lng], tooltip='목적지').add_to(m)


# Tmap API 키
tmap_api_key = 'QaALuzWbgm8PXyhzGSGgM9HHtAdgGuGL7JWocrK9'

# Tmap API 경로 요청 URL 생성
url = f'https://apis.openapi.sk.com/tmap/routes/pedestrian?version=1&format=json&appKey={tmap_api_key}&startX={start_lng}&startY={start_lat}&startName=출발지&endX={end_lng}&endY={end_lat}&endName=목적지&searchOption=0'
# 경로탐색 시 우선순위 옵션 -> searchOption
# - 00 : 교통최적 + 추천 (기본 값)
# - 01 : 교통최적 + 무료우선
# - 02 : 교통최적 + 최소시간
# - 03 : 교통최적 + 초보
# - 04 : 교통최적 + 고속도로우선
# - 10 : 최단거리 + 유/무료
# - 19 : 교통최적 + 어린이보호구역 회피
response = requests.get(url)
data = response.json()

coordinates = []
for feature in data['features']:
    if feature['geometry']['type'] == 'LineString':
        coordinates.extend([(coord[1], coord[0]) for coord in feature['geometry']['coordinates']])

print(coordinates)
print(len(coordinates))
polyline = folium.PolyLine(locations=coordinates, color='blue', weight=5).add_to(m)
plugins.PolyLineTextPath(
    polyline,
    text='>',
    repeat='50px',
    offset=7,
    attributes={'fill': 'red', 'font-weight': 'bold', 'font-size': '12'},
).add_to(m)


# MarkerCluster object - marker 표시
marker_cluster = MarkerCluster()


# color argument of Icon should be one of:
# {'black', 'white', 'green', 'lightgreen', 'darkred', 'lightred', 'cadetblue', 'red', 'darkpurple',
# 'orange', 'purple', 'darkgreen', 'blue', 'lightgray', 'pink', 'gray', 'lightblue', 'beige', 'darkblue'}


cctv_data_file = r"C:\Users\minsoo\OneDrive - 창원대학교\바탕 화면\창원 빅데이터 공모전\data\창원cctv_data.csv"
cctv_df = pd.read_csv(cctv_data_file, encoding='utf-8')
cctv_locations = cctv_df[['WGS84위도', 'WGS84경도', '촬영방면']]

# CCTV 위치 - Marker
for _, row in cctv_locations.iterrows():
    lat, lon = row['WGS84위도'], row['WGS84경도']
    popup_text = f'CCTV <br> 위도: {lat} <br> 경도: {lon}'  # 팝업에 표시할 텍스트
    iframe_html = f'<iframe width="100%" height="315" src="http://www.utic.go.kr/view/map/cctvStream.jsp?' \
                  f'cctvid=L250001&cctvname=KBS%25EC%2582%25AC%25EA%25B1%25B0%25EB%25A6%25AC&kind=Y&cctvip=140' \
                  f'&cctvch=12&id=null&cctvpasswd=null&cctvport=null&minX=128.59823203434868&minY=35.188051060156894' \
                  f'&maxX=128.74501945865873&maxY=35.2574447382778" frameborder="0" allowfullscreen></iframe>'

    if lat == 35.22875:
        popup_html = f'<div id="cctv-video" style="width: 370px; height: 370px; background-color: white; ' \
                     f'font-size: 12px;">{popup_text}<br>{iframe_html}</div>'
    else:
        popup_html = f'<div style="width: 150px; height: 45px; background-color: white; ' \
                     f'font-size: 12px;">{popup_text}</div>'

    folium.Marker([lat, lon], icon=folium.Icon(color='lightblue'),
                  popup=folium.Popup(popup_html, max_width=400)).add_to(marker_cluster)


police_data_file = r"C:\Users\minsoo\OneDrive - 창원대학교\바탕 화면\창원 빅데이터 공모전\data\창원police_data.csv"
police_df = pd.read_csv(police_data_file, encoding='utf-8')
police_locations = police_df[['위도', '경도', '경찰서이름', '치안사고등급']]

# Police 위치 - Marker
for _, row in police_locations.iterrows():
    lat, lon, police_station_name = row['위도'], row['경도'], row['경찰서이름']
    popup_text = f'{police_station_name}<br>위도: {lat}<br>경도: {lon}'

    popup_html = f'<div style="width: 150px; height: 47px; background-color: white; font-size: 12px;">{popup_text}</div>'

    folium.Marker([lat, lon], icon=folium.Icon(color='blue'),
                  popup=folium.Popup(popup_html, max_width=250)).add_to(marker_cluster)


fire_data_file = r"C:\Users\minsoo\OneDrive - 창원대학교\바탕 화면\창원 빅데이터 공모전\data\창원fire_data.csv"
fire_df = pd.read_csv(fire_data_file, encoding='utf-8')
fire_locations = fire_df[['위도', '경도', '소방서이름']]

# Fire 위치 - Marker
for _, row in fire_locations.iterrows():
    lat, lon, fire_station_name = row['위도'], row['경도'], row['소방서이름']
    popup_text = f'{fire_station_name}<br>위도: {lat}<br>경도: {lon}'

    popup_html = f'<div style="width: 150px; height: 47px; background-color: white; font-size: 12px;">{popup_text}</div>'

    folium.Marker([lat, lon], icon=folium.Icon(color='cadetblue'),
                  popup=folium.Popup(popup_html, max_width=250)).add_to(marker_cluster)


store_data_file = r"C:\Users\minsoo\OneDrive - 창원대학교\바탕 화면\창원 빅데이터 공모전\data\geocoded_addresses_store.csv"
store_df = pd.read_csv(store_data_file, encoding='utf-8')
store_locations = store_df[['위도', '경도']]

# Store 위치 - Marker
for _, row in store_locations.iterrows():
    lat, lon = row['위도'], row['경도']
    popup_text = f'편의점 <br> 위도: {lat}<br> 경도: {lon}'

    popup_html = f'<div style="width: 150px; height: 47px; background-color: white; font-size: 12px;">{popup_text}</div>'

    folium.Marker([lat, lon], icon=folium.Icon(color='cadetblue'),
                  popup=folium.Popup(popup_html, max_width=250)).add_to(marker_cluster)


marker_cluster.add_to(m)


interval = 10

for i in range(interval):
    start_idx = i * len(coordinates) // interval
    end_idx = (i + 1) * len(coordinates) // interval
    end_idx = min(end_idx, len(coordinates) - 1)

    start_coord = coordinates[start_idx]
    end_coord = coordinates[end_idx]

    distance_2r = haversine.hs(start_coord[0], start_coord[1], end_coord[0], end_coord[1])
    circle_center = ((start_coord[0] + end_coord[0]) / 2, (start_coord[1] + end_coord[1]) / 2)
    print("diameter:", distance_2r, "circle_center:", circle_center)

    # 원 안에 있는 CCTV, police, fire, store -> count
    cctv_station_count, cctv_station_count_dir = 0, 0
    police_station_count, police_station_count_security = 0, 0
    fire_station_count = 0
    store_station_count = 0

    for _, cctv_row in cctv_locations.iterrows():
        cctv_lat, cctv_lon, cctv_dir = cctv_row['WGS84위도'], cctv_row['WGS84경도'], cctv_row['촬영방면']
        if haversine.hs(circle_center[0], circle_center[1], cctv_lat, cctv_lon) <= (distance_2r / 2):
            cctv_station_count += 1
            cctv_station_count_dir += 1 + 0.01 * cctv_dir

    for _, police_row in police_locations.iterrows():
        police_lat, police_lon, police_security = police_row['위도'], police_row['경도'], police_row['치안사고등급']
        if haversine.hs(circle_center[0], circle_center[1], police_lat, police_lon) <= (distance_2r / 2):
            police_station_count += 1
            police_station_count_security += police_security * (-0.0005)

    for _, fire_row in fire_locations.iterrows():
        fire_lat, fire_lon = fire_row['위도'], fire_row['경도']
        if haversine.hs(circle_center[0], circle_center[1], fire_lat, fire_lon) <= (distance_2r / 2):
            fire_station_count += 1

    for _, store_row in store_locations.iterrows():
        store_lat, store_lon = store_row['위도'], store_row['경도']
        if haversine.hs(circle_center[0], circle_center[1], store_lat, store_lon) <= (distance_2r / 2):
            store_station_count += 1

    print("cctv_count:", cctv_station_count, "police_count:", police_station_count, "fire_count:", fire_station_count, "store_count:", store_station_count)

    circle_area = math.pi * ((distance_2r / 2) ** 2) * 500
    # 안전지수 = { (CCTV_count * 1.(0.01 ~ 0.n) + 경찰서_count * (w: 2.0) + 편의점_count + 소방서_count) / circle_area } + 1~4(:등급)*(-0.0005)
    safety_index = (cctv_station_count_dir + (police_station_count * 2.0) + fire_station_count + store_station_count) / circle_area + police_station_count_security
    print("circle_area:", circle_area, "안전지수:", safety_index, '\n')

    # 안전지수에 따른 마커 표시
    if safety_index >= 0.04:
        circle_color = 'green'
    elif safety_index >= 0.02:
        circle_color = 'orange'
    else:
        circle_color = 'red'

    circle = folium.Circle(
        circle_center, radius=(distance_2r / 2) * 1000, color=circle_color, fill=True, fill_opacity=0.2
    )
    circle.add_to(m)
    folium.Marker(circle_center, icon=folium.Icon(color=circle_color), tooltip=f'안전지수: {safety_index:.2f}').add_to(m)


m.save('safe_path_tmap.html')