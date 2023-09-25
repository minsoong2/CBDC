import requests
import csv


def get_geocode(address):

    client_id = 'a0lrtua0a3'
    client_secret = '3BKNDSMe8An3ZZPdbzthZPRSBfWIYPu31POUGXDL'

    # 도로명 주소 인코딩 -> URL 생성
    encoded_address = requests.utils.quote(address)

    # API 호출 URL
    url = f'https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?query={encoded_address}'

    # HTTP 요청 헤더
    headers = {
        'X-NCP-APIGW-API-KEY-ID': client_id,
        'X-NCP-APIGW-API-KEY': client_secret,
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    print(data)

    # 위도 경도 추출
    if data.get('status') == 'OK' and data.get('addresses'):
        location = data['addresses'][0]
        latitude = location['y'] # 위도
        longitude = location['x'] # 경도
        return latitude, longitude
    else:
        print('주소를 찾을 수 없습니다.')
        return None, None


# 변경
file_path = 'C:/Users/minsoo/OneDrive - 창원대학교/바탕 화면/fire_location.txt'
data_to_save = []

with open(file_path, 'r', encoding='utf-8') as file:
    addresses = file.readlines()
    for address in addresses:
        address = address.strip()  # 줄 바꿈 문자 제거
        latitude, longitude = get_geocode(address)
        if latitude is not None and longitude is not None:
            data_to_save.append([address, latitude, longitude])
        else:
            print(address)

# CSV 파일로 저장 - 변경
with open('C:/Users/minsoo/OneDrive - 창원대학교/바탕 화면/geocoded_addresses_fire.csv', 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['도로명 주소', '위도', '경도'])
    csv_writer.writerows(data_to_save)