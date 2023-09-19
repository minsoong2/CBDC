# 파일 경로 설정
file_path = 'C:/Users/minsoo/OneDrive - 창원대학교/바탕 화면/police_location.txt'

with open(file_path, 'r', encoding='utf-8') as file:
    content = file.read()

content = content.replace('  ', ' ')

with open(file_path, 'w', encoding='utf-8') as file:
    file.write(content)
