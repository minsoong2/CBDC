# 두 지점 간의 위도와 경도를 사용하여 두 지점 사이의 대원거리(또는 직선 거리)를 구하는 수학적인 공식
# 지구를 구로 가정하고 두 점 간의 곡선 거리를 계산하는 데 사용
# a = sin²(Δlat/2) + cos(lat1) * cos(lat2) * sin²(Δlon/2)
# c = 2 * atan2(√a, √(1-a))
# distance = radius * c
import math


def hs(lat1, lon1, lat2, lon2):
    # 지구 radius
    radius = 6371  # km
    dlat, dlon = math.radians(lat2) - math.radians(lat1), math.radians(lon2) - math.radians(lon1)

    # Haversine 공식
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = radius * c

    return distance


