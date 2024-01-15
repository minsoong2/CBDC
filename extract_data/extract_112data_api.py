import requests
import xml.etree.ElementTree as ET

key = "jFxUmY3J1D8g9f9z%2FOXDX%2B0yHqscOP6dw%2FZJjYkW%2FSrcBKXIlh1PeEVhWANEbElQllrvJg70msKqf8%2FqFMjWew%3D%3D"
page = 1
url = "http://apis.data.go.kr/6480000/gyeongnampoliceoffice/gyeongnampoliceofficeList?serviceKey=" + \
      key + f"&numOfRows=10&pageNo={page}"
call = requests.get(url)
document = call.text
root = ET.fromstring(document)
item_count = int(root.find('.//totalCount').text) // 10 + 1

f = open('../road_address_api.txt', 'w', encoding='utf-8')

for p in range(1, item_count + 1):
      url = "http://apis.data.go.kr/6480000/gyeongnampoliceoffice/gyeongnampoliceofficeList?serviceKey=" + \
            key + f"&numOfRows=10&pageNo={p}"
      call = requests.get(url)
      document = call.text
      root = ET.fromstring(document)
      for r_a in root.iter('roadaddress'):
            print(r_a.text)
            f.write(r_a.text + '\n')