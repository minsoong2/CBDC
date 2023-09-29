import pandas as pd

cctv_data_file = r"C:\Users\minsoo\OneDrive - 창원대학교\바탕 화면\창원cctv_data.csv"
cctv_df = pd.read_csv(cctv_data_file, encoding='utf-8')
# null인 행을 1로 채우기
cctv_df['촬영방면'].fillna(1, inplace=True)
cctv_df.to_csv('C:/Users/minsoo/OneDrive - 창원대학교/바탕 화면/창원cctv_data_new.csv', index=False, encoding='utf-8-sig')
print('clear')