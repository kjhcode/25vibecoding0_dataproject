import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import koreanize_matplotlib

st.set_page_config(layout="wide", page_title="서울특별시 인구 연령별 시각화")

st.title("서울특별시 연령별 인구 시각화 (Plotly)")

# 데이터 불러오기
@st.cache_data
def load_data():
    df_all = pd.read_csv("202504_202504_연령별인구현황_남녀합계.csv", encoding="cp949")
    df_sex = pd.read_csv("202504_202504_연령별인구현황_월간_남녀구분.csv", encoding="cp949")
    return df_all, df_sex

df_all, df_sex = load_data()

# (1) 서울특별시만 필터
total_row = df_all[df_all['행정구역'].str.contains('서울특별시 ')].iloc[0]
sex_row = df_sex[df_sex['행정구역'].str.contains('서울특별시 ')].iloc[0]

# (2) 연령 컬럼만 추출 (문자열 변환 → 쉼표제거 → 숫자형)
age_cols = [col for col in df_all.columns if '계_' in col and ('세' in col or '100세' in col)]
ages = [col.split('_')[-1] for col in age_cols]
age_counts = total_row[age_cols].astype(str).str.replace(',', '').astype(int)

# (3) 남녀 별도 추출 (문자열 변환 → 쉼표제거 → 숫자형)
male_cols = [col for col in df_sex.columns if '남_' in col and ('세' in col or '100세' in col)]
female_cols = [col for col in df_sex.columns if '여_' in col and ('세' in col or '100세' in col)]
male_counts = sex_row[male_cols].astype(str).str.replace(',', '').astype(int)
female_counts = sex_row[female_cols].astype(str).str.replace(',', '').astype(int)

# =====================
# 1) 연령별 전체 인구 막대그래프
# =====================
fig1 = go.Figure()
fig1.add_trace(go.Bar(x=ages, y=age_counts, name="전체 인구"))
fig1.update_layout(title="연령별 전체 인구 분포 (서울특별시)", xaxis_title="연령", yaxis_title="인구수")

st.plotly_chart(fig1, use_container_width=True)

# =====================
# 2) 남녀 인구 피라미드
# =====================
fig2 = go.Figure()

fig2.add_trace(go.Bar(y=ages, x=-male_counts, name="남성", orientation='h', marker_color='royalblue'))
fig2.add_trace(go.Bar(y=ages, x=female_counts, name="여성", orientation='h', marker_color='pink'))

fig2.update_layout(
    title="연령별 남녀 인구 피라미드 (서울특별시)",
    barmode='relative',
    xaxis=dict(
        title='인구수',
        tickvals=[-20000, -10000, 0, 10000, 20000],
        ticktext=['20,000', '10,000', '0', '10,000', '20,000']
    ),
    yaxis=dict(title='연령'),
    legend=dict(x=0.8, y=0.9)
)

st.plotly_chart(fig2, use_container_width=True)
