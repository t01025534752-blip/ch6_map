import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import numpy as np

# 앱 제목 설정
st.title("🚇 부산 지하철 역별 이용객수 지도 분석 앱")

# ① CSV 파일 업로드 및 데이터 표 표시
uploaded_file = st.file_uploader("busan_subway.csv 파일을 업로드하세요", type=["csv"])

if uploaded_file is not None:
    # 업로드된 CSV 파일을 판다스 데이터프레임으로 읽기
    df = pd.read_csv(uploaded_file)
    
    st.subheader("📋 전체 지하철 이용객 데이터")
    st.dataframe(df)
    
    # [호선 필터] multiselect로 원하는 호선 선택 기능 추가
    lines = df['호선'].unique().tolist()
    selected_lines = st.multiselect("표시할 호선을 선택하세요", lines, default=lines)
    
    # 선택된 호선만 데이터 필터링
    filtered_df = df[df['호선'].isin(selected_lines)]
    
    # [색상] 호선별 색 지정 함수 (1호선: 주황, 2호선: 초록, 3호선: 갈색, 4호선: 파랑)
    def get_line_color(line):
        if '1호선' in str(line):
            return 'orange'
        elif '2호선' in str(line):
            return 'green'
        elif '3호선' in str(line):
            return 'saddlebrown'
        elif '4호선' in str(line):
            return 'blue'
        else:
            return 'gray'

    # ② Folium 지도 생성 (부산 중심 좌표 기준)
    m = folium.Map(location=[35.1796, 129.0756], zoom_start=11)
    
    # 역마다 CircleMarker 표시 (원의 면적이 이용객수에 비례하도록 제곱근 활용)
    for idx, row in filtered_df.iterrows():
        # 면적이 이용객수에 비례하려면 반지름은 제곱근(sqrt) 값에 비례해야 합니다.
        radius = float(np.sqrt(row['이용객수']) * 0.15)
        color = get_line_color(row['호선'])
        
        folium.CircleMarker(
            location=[row['위도'], row['경도']],
            radius=max(radius, 3), # 너무 작아지지 않도록 최소 크기 3 보장
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.6,
            tooltip=row['역명'], # ③ 마우스를 올리면 역명 표시
            popup=f"역명: {row['역명']}<br>호선: {row['호선']}<br>이용객수: {row['이용객수']:,}명" # 클릭하면 상세 이용객수 표시
        ).add_to(m)
        
    # 지도 시각화 출력
    st.subheader("🗺️ 부산 지하철 지도 분석")
    st_folium(m, width=700, height=500)
    
    # [표] 이용객 상위 5개 역 표 표시
    st.subheader("🏆 이용객 상위 5개 역")
    top5_df = filtered_df.sort_values(by='이용객수', ascending=False).head(5)
    st.table(top5_df[['호선', '역명', '이용객수']])

else:
    st.info("시작하려면 'busan_subway.csv' 파일을 업로드해주세요.")