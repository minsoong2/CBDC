import pandas as pd
import re


excel_file_path = r"C:\Users\minsoo\OneDrive - 창원대학교\바탕 화면\경상남도 창원시_CCTV설치 현황(2022.11 _ 2023.07).xlsx"
df = pd.read_excel(excel_file_path)

selected_columns = ["번호", "소재지도로명주소", "WGS84위도", "WGS84경도", "촬영방면정보"]
df_selected = df[selected_columns].copy()
df_selected['촬영방면'] = df_selected['촬영방면정보'].apply(lambda x: ''.join(re.findall(r'\d', str(x))))
df_selected.drop(columns=["촬영방면정보"], inplace=True)

output_csv_path = r"C:\Users\minsoo\OneDrive - 창원대학교\바탕 화면\창원cctv_data.csv"
df_selected.to_csv(output_csv_path, index=False, encoding='utf-8-sig')

print("clear")
