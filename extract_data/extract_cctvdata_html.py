import pandas as pd
import folium

excel_file_path = r"C:\Users\minsoo\OneDrive - 창원대학교\바탕 화면\경상남도 창원시_CCTV설치 현황(2022.11 _ 2023.07).xlsx"
df = pd.read_excel(excel_file_path)
selected_columns = ["번호", "소재지도로명주소", "WGS84위도", "WGS84경도"]
df_selected = df[selected_columns]
m = folium.Map(location=[df_selected["WGS84위도"].mean(), df_selected["WGS84경도"].mean()], zoom_start=12)

for _, row in df_selected.iterrows():
    folium.Marker([row["WGS84위도"], row["WGS84경도"]], tooltip=row["소재지도로명주소"]).add_to(m)

output_html_path = r"C:\Users\minsoo\OneDrive - 창원대학교\바탕 화면\cctv_map.html"
m.save(output_html_path)

print("clear")