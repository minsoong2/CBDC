import requests
import folium
from folium import plugins
import math


def haversine(lat1, lon1, lat2, lon2):
    # 지구의 반경 (지구의 반경은 평균 반경을 사용합니다)
    radius = 6371  # 지구 반경 (단위: 킬로미터)

    # 라디안으로 변환
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # 위도와 경도의 차이 계산
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Haversine 공식을 사용하여 거리 계산
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = radius * c

    return distance


start_lat = 35.22241510564285
start_lng = 128.6879361625245
end_lat = 35.236619713404615
end_lng = 128.69428289085678
stopover_lat = 37.5675000  # 경유지 위도
stopover_lng = 126.9790000  # 경유지 경도

m = folium.Map(location=[start_lat, start_lng], zoom_start=15)
folium.Marker([start_lat, start_lng], tooltip='출발지').add_to(m)
folium.Marker([end_lat, end_lng], tooltip='목적지').add_to(m)
folium.Marker([stopover_lat, stopover_lng], tooltip='경유지').add_to(m)

# Tmap API 키
tmap_api_key = 'QaALuzWbgm8PXyhzGSGgM9HHtAdgGuGL7JWocrK9'

# Tmap API 경로 요청 URL 생성
url = f'https://apis.openapi.sk.com/tmap/routes/pedestrian?version=1&format=json&appKey={tmap_api_key}&startX={start_lng}&startY={start_lat}&startName=출발지&endX={end_lng}&endY={end_lat}&endName=목적지&searchOption=0'
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

# 1번째 ">"와 10번째 ">"의 좌표
coord_1st_arrow = (coordinates[0][0], coordinates[0][1])  # 1번째 ">"
coord_10th_arrow = (coordinates[9][0], coordinates[9][1])  # 10번째 ">"

# 거리 계산 (예: haversine 함수 사용)
distance_between_arrows = haversine(coord_1st_arrow[0], coord_1st_arrow[1], coord_10th_arrow[0], coord_10th_arrow[1])

# Folium 지도에 원 그리기
circle = folium.Circle(coord_1st_arrow, radius=distance_between_arrows*1000, color='red', fill=True, fill_opacity=0.2)
circle.add_to(m)

m.save('safe_path_tmap.html')
