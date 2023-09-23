import pandas as pd

input_file_path = r'C:\Users\minsoo\OneDrive - 창원대학교\바탕 화면\geocoded_addresses.csv'
output_file_path = r'C:\Users\minsoo\OneDrive - 창원대학교\바탕 화면\창원police_data.csv'

df = pd.read_csv(input_file_path, encoding='cp949')

filtered_df = df[df['도로명 주소'].str.contains('창원시', case=False, na=False)]
filtered_df.to_csv(output_file_path, index=False, encoding='utf-8-sig')

print('clear')
