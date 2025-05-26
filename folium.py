
# streamlit_folium_app.py

import streamlit as st
import folium
from streamlit_folium import st_folium
import geopandas as gpd
import pandas as pd

# 제목
st.title("지도 데이터 분석 웹 앱")
st.markdown("Folium과 Streamlit을 사용하여 지도 데이터를 분석하고 시각화합니다.")

# GeoJSON 또는 shapefile 업로드
uploaded_file = st.file_uploader("GeoJSON 또는 Shapefile(.zip) 업로드", type=["geojson", "zip"])

if uploaded_file:
    if uploaded_file.name.endswith(".geojson"):
        gdf = gpd.read_file(uploaded_file)
    elif uploaded_file.name.endswith(".zip"):
        gdf = gpd.read_file(f"zip://{uploaded_file.name}")
    
    # 기본 정보 표시
    st.subheader("데이터 요약")
    st.write(gdf.head())
    st.map(gdf)

    # Folium 맵 생성
    st.subheader("Folium 지도")
    m = folium.Map(location=[gdf.geometry.centroid.y.mean(), gdf.geometry.centroid.x.mean()], zoom_start=10)
    
    folium.GeoJson(gdf).add_to(m)

    # 지도 표시
    st_data = st_folium(m, width=700, height=500)

    # 속성별 통계 선택
    numeric_columns = gdf.select_dtypes(include='number').columns.tolist()
    if numeric_columns:
        selected_column = st.selectbox("통계 분석할 열 선택", numeric_columns)
        st.write(f"{selected_column} 열의 통계:")
        st.write(gdf[selected_column].describe())
else:
    st.warning("먼저 GeoJSON 또는 Shapefile(.zip)을 업로드해주세요.")
