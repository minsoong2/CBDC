import csv

path = "C:/Users/minsoo/OneDrive - 창원대학교/바탕 화면/경찰청_경찰관서 위치 주소 현황_20230811.csv"
f = open('../road_address_csv.txt', 'w', encoding='utf-8')
found_rows = []
with open(path, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    for row in csv_reader:
        if row['시도청'] == '경남청':
            found_rows.append(row)

road_address = []
for row in found_rows:
    road_address.append(row['주소'])
    print(row['주소'])
    f.write(row['주소'] + '\n')