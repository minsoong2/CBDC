import requests
import folium
from folium import plugins

start_lat = 37.5666102
start_lng = 126.9783881
end_lat = 37.5662952
end_lng = 126.9757329
stopover_lat = 37.5675000  # 경유지 위도
stopover_lng = 126.9790000  # 경유지 경도

m = folium.Map(location=[start_lat, start_lng], zoom_start=15)
folium.Marker([start_lat, start_lng], tooltip='출발지').add_to(m)
folium.Marker([end_lat, end_lng], tooltip='목적지').add_to(m)
folium.Marker([stopover_lat, stopover_lng], tooltip='경유지').add_to(m)

# Tmap API 키
tmap_api_key = 'QaALuzWbgm8PXyhzGSGgM9HHtAdgGuGL7JWocrK9'

# Tmap API 경로 요청 URL 생성
url = f'https://apis.openapi.sk.com/tmap/routes/pedestrian?version=1&format=json&appKey={tmap_api_key}&startX={start_lng}&startY={start_lat}&startName=출발지&passList={stopover_lng},{stopover_lat}&endX={end_lng}&endY={end_lat}&endName=목적지&searchOption=0'
# 경로탐색 시 우선순위 옵션 -> searchOption
# - 00 : 교통최적+추천 (기본 값)
# - 01 : 교통최적+무료우선
# - 02 : 교통최적+최소시간
# - 03 : 교통최적+초보
# - 04 : 교통최적+고속도로우선
# - 10 : 최단거리+유/무료
# - 19 : 교통최적+어린이보호구역 회피

response = requests.get(url)
data = response.json()
print(data)

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

m.save('route_map_with_stopover_tmap.html')