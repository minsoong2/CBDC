import requests
import folium
from folium import plugins
import pandas as pd
import haversine
import math
from folium.plugins import MarkerCluster

start_lat = 35.22241510564285
start_lng = 128.6879361625245
end_lat = 35.236619713404615
end_lng = 128.69428289085678

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

cctv_data_file = r"C:\Users\minsoo\OneDrive - 창원대학교\바탕 화면\창원cctv_data.csv"
cctv_df = pd.read_csv(cctv_data_file)
cctv_locations = cctv_df[['WGS84위도', 'WGS84경도']]

# CCTV 위치 - Marker
for _, row in cctv_locations.iterrows():
    lat, lon = row['WGS84위도'], row['WGS84경도']
    folium.Marker([lat, lon], icon=folium.Icon(color='lightblue'), tooltip='CCTV 위치').add_to(marker_cluster)

police_data_file = r"C:\Users\minsoo\OneDrive - 창원대학교\바탕 화면\창원police_data.csv"
police_df = pd.read_csv(police_data_file)
police_locations = police_df[['위도', '경도']]

# Police 위치 - Marker
for _, row in police_locations.iterrows():
    lat, lon = row['위도'], row['경도']
    folium.Marker([lat, lon], icon=folium.Icon(color='blue'), tooltip='경찰서 위치').add_to(marker_cluster)

marker_cluster.add_to(m)

interval = 10

for i in range(interval):
    start_idx = i * len(coordinates) // interval
    end_idx = (i + 1) * len(coordinates) // interval
    end_idx = min(end_idx, len(coordinates) - 1)

    start_coord = coordinates[start_idx]
    end_coord = coordinates[end_idx]

    distance_between_arrows = haversine.hs(start_coord[0], start_coord[1], end_coord[0], end_coord[1])
    circle_center = ((start_coord[0] + end_coord[0]) / 2, (start_coord[1] + end_coord[1]) / 2)

    # 원 안에 있는 CCTV와 경찰서 수 count
    cctv_count = 0
    police_station_count = 0

    for _, cctv_row in cctv_locations.iterrows():
        cctv_lat, cctv_lon = cctv_row['WGS84위도'], cctv_row['WGS84경도']
        if haversine.hs(circle_center[0], circle_center[1], cctv_lat, cctv_lon) <= distance_between_arrows * 500:
            cctv_count += 1

    for _, police_row in police_locations.iterrows():
        police_lat, police_lon = police_row['위도'], police_row['경도']
        if haversine.hs(circle_center[0], circle_center[1], police_lat, police_lon) <= distance_between_arrows * 500:
            police_station_count += 1

    # 안전지수 = (CCTV_count + 경찰서_count) / 원의 면적
    circle_area = math.pi * (distance_between_arrows * 500) ** 2
    safety_index = (cctv_count + police_station_count) / circle_area

    # 안전지수에 따른 마커 표시
    if safety_index >= 0.1:
        circle_color = 'green'
    elif safety_index >= 0.05:
        circle_color = 'orange'
    else:
        circle_color = 'red'

    circle = folium.Circle(
        circle_center, radius=distance_between_arrows * 500, color=circle_color, fill=True, fill_opacity=0.2
    )
    circle.add_to(m)
    folium.Marker(circle_center, icon=folium.Icon(color=circle_color), tooltip=f'안전지수: {safety_index:.2f}').add_to(m)

# 안전지수에 대해 고려할 것
# !!!범죄율!!!과 인구 밀도 고려 지수: 범죄율과 지역 인구 밀도를 고려한 복합 지수 -> 안전지수 = (인구 밀도 * (1 - 범죄율))
# cctv방면 1~8
# 소방서 및 24시간 편의점

m.save('safe_path_tmap.html')