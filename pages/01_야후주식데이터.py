import streamlit as st
import yfinance as yf
import pandas as pd
import datetime

# -------------------------------
# 1. 날짜 입력
# -------------------------------
st.title("📈 야후 주식 데이터 분석")

today = datetime.date.today()
default_start = today - datetime.timedelta(days=365)

start_date = st.date_input("시작 날짜", default_start)
end_date = st.date_input("종료 날짜", today)

# -------------------------------
# 2. 종목 리스트
# -------------------------------
top10 = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Google": "GOOGL",
    "Amazon": "AMZN",
    "Tesla": "TSLA",
    "Meta": "META",
    "NVIDIA": "NVDA",
    "Berkshire": "BRK-B",
    "JPMorgan": "JPM",
    "Visa": "V"
}

selected = st.multiselect("🔎 종목 선택", options=list(top10.keys()), default=list(top10.keys())[:5])
tickers = [top10[name] for name in selected]

if not selected:
    st.warning("최소 하나 이상의 종목을 선택해 주세요.")
    st.stop()

# -------------------------------
# 3. 데이터 다운로드 함수
# -------------------------------
@st.cache_data
def download_valid_data(tickers, start, end):
    valid_data = {}
    for ticker in tickers:
        try:
            data = yf.download(ticker, start=start, end=end)['Adj Close']
            if not data.empty:
                valid_data[ticker] = data
        except:
            pass
    return pd.DataFrame(valid_data)

with st.spinner("데이터 다운로드 중..."):
    data = download_valid_data(tickers, start_date, end_date)

# -------------------------------
# 4. 이동평균선 설정
# -------------------------------
ma_period = st.slider("이동평균 기간 (일)", min_value=5, max_value=100, value=20)

# -------------------------------
# 5. 시각화
# -------------------------------
if not data.empty:
    st.subheader("📊 조정 종가 (Adj Close)")
    st.line_chart(data)

    # -------------------------------
    # 6. 이동평균선 계산 및 시각화
    # -------------------------------
    st.subheader(f"📈 {ma_period}일 이동평균선")
    ma_data = data.rolling(window=ma_period).mean()
    st.line_chart(ma_data)

    # -------------------------------
    # 7. 수익률 계산 및 출력
    # -------------------------------
    st.subheader("📉 종목별 수익률 (%)")
    returns = ((data.iloc[-1] - data.iloc[0]) / data.iloc[0]) * 100
    returns_df = returns.to_frame(name='수익률').round(2).sort_values(by='수익률', ascending=False)
    st.dataframe(returns_df)

    # -------------------------------
    # 8. CSV 다운로드 기능
    # -------------------------------
    st.download_button(
        label="📥 CSV로 데이터 다운로드",
        data=data.to_csv().encode('utf-8-sig'),
        file_name="주식_데이터.csv",
        mime='text/csv'
    )
else:
    st.error("유효한 종목 데이터가 없습니다. 종목 코드를 확인해주세요.")
