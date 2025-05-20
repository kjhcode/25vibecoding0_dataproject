import streamlit as st
import yfinance as yf
import pandas as pd
import datetime

# -------------------------------
# 1. 날짜 입력
# -------------------------------
st.title("야후 주식 데이터 분석")

today = datetime.date.today()
default_start = today - datetime.timedelta(days=365)

start_date = st.date_input("시작 날짜", default_start)
end_date = st.date_input("종료 날짜", today)

# -------------------------------
# 2. 종목 리스트 (예시로 top10 미리 지정)
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

selected = st.multiselect("종목 선택", options=list(top10.keys()), default=list(top10.keys())[:5])

if not selected:
    st.warning("최소 하나 이상의 종목을 선택해 주세요.")
    st.stop()

tickers = [top10[name] for name in selected]

# -------------------------------
# 3. 데이터 다운로드 및 검증
# -------------------------------
@st.cache_data
def download_valid_data(tickers, start, end):
    valid_data = {}
    for ticker in tickers:
        try:
            data = yf.download(ticker, start=start, end=end)['Adj Close']
            if not data.empty:
                valid_data[ticker] = data
        except Exception as e:
            st.warning(f"{ticker} 다운로드 실패: {e}")
    return pd.DataFrame(valid_data)

with st.spinner("데이터 다운로드 중..."):
    data = download_valid_data(tickers, start_date, end_date)

# -------------------------------
# 4. 시각화
# -------------------------------
if not data.empty:
    st.subheader("종목별 조정 종가")
    st.line_chart(data)
else:
    st.error("선택한 종목에 대한 유효한 데이터가 없습니다.")

