# main.py
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from layer import add_brand_layers

# ブランド地区データ
brand_areas = pd.DataFrame({
    'brand': ['治安の良い地区', '公園の多い地区', '大型の一戸建ての多い地区', '文教地区'],
    'latitude': [35.6895, 35.6995, 35.7095, 35.7195],
    'longitude': [139.6917, 139.7017, 139.7117, 139.7217]
})

# マイナスのブランド地区データ
negative_areas = pd.DataFrame({
    'brand': ['治安の悪い地区', 'ハザードマップの水害危険地区'],
    'latitude': [35.6890, 35.6980],
    'longitude': [139.6900, 139.7000],
    'radius': [1200, 500]  # メートル単位の半径
})

# 仮のポリゴンデータ
polygons = [
    [(35.7095, 139.7007), (35.6695, 139.7427), (35.6295, 139.6917), (35.6595, 139.6717)],  # 治安の良い地区
    [(35.7095, 139.7417), (35.6795, 139.7717), (35.6695, 139.7417), (35.6995, 139.7217)],  # 公園の多い地区
    [(35.7335, 139.7217), (35.7095, 139.7617), (35.6595, 139.7117), (35.7195, 139.6917)],  # 大型の一戸建ての多い地区
    [(35.7805, 139.7217), (35.7495, 139.7417), (35.7295, 139.7117), (35.7695, 139.6817)]   # 文教地区
]

# 地図の初期設定
map_center = [35.6895, 139.6917]
m = folium.Map(location=map_center, zoom_start=12)

# ブランド地区の選択
st.sidebar.title("ブランド地区の選択")
selected_brands = []
for brand in brand_areas['brand']:
    if st.sidebar.checkbox(brand, False):  # デフォルトでオフに設定
        selected_brands.append(brand)

# ネガティブエリアの選択
st.sidebar.title("ネガティブエリアの選択")
selected_negative_brands = []
for brand in negative_areas['brand']:
    if st.sidebar.checkbox(brand, False):  # デフォルトでオフに設定
        selected_negative_brands.append(brand)

# 選択されたブランド地区のみをフィルタリング
selected_brand_areas = brand_areas[brand_areas['brand'].isin(selected_brands)]

# 選択されたインデックスに基づいてポリゴンをフィルタリング
selected_indices = selected_brand_areas.index.tolist()
selected_polygons = [polygons[i] for i in selected_indices]

# 選択されたネガティブエリアのみをフィルタリング
selected_negative_areas = negative_areas[negative_areas['brand'].isin(selected_negative_brands)]

# 選択されたブランド地区とネガティブエリアのレイヤーを追加
m = add_brand_layers(m, selected_brand_areas, selected_polygons, selected_negative_areas)

# 地図を表示
folium_static(m)