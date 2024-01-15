import folium
import requests

# 출발지, 목적지, 경유지 좌표 설정
start_lat = 37.5666102
start_lng = 126.9783881
end_lat = 37.5662952
end_lng = 126.9757329

stopover_lat = 37.5675000  # 경유지 위도
stopover_lng = 126.9790000  # 경유지 경도

# 지도 초기 위치 설정
m = folium.Map(location=[start_lat, start_lng], zoom_start=15)

# 출발지와 목적지 마커 표시
folium.Marker([start_lat, start_lng], tooltip='출발지').add_to(m)
folium.Marker([end_lat, end_lng], tooltip='목적지').add_to(m)
folium.Marker([stopover_lat, stopover_lng], tooltip='경유지').add_to(m)

# 경로 설정
url = f'https://naveropenapi.apigw.ntruss.com/map-direction/v1/driving?start={start_lng},{start_lat}&goal={end_lng},{end_lat}&waypoints={stopover_lng},{stopover_lat}'
naver_api_key = 'Jj1YcLnFwgXZDb2OWeK03Ys0cMM2Sw3lgcoOMJgC'

headers = {
    'X-NCP-APIGW-API-KEY-ID': 'go8pjhi6d3',
    'X-NCP-APIGW-API-KEY': naver_api_key
}

response = requests.get(url, headers=headers)
data = response.json()

path = data['route']['traoptimal'][0]['path']
print(path)
path_coords = [(coord[1], coord[0]) for coord in path]
print(path_coords)
print(len(path_coords))
folium.PolyLine(locations=path_coords, color='blue', weight=5).add_to(m)

m.save('route_map_with_stopover_naver.html')
