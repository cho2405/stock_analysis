from pykrx import stock
tickers = stock.get_market_ticker_list()
print(tickers)

종목 = []
for i in tickers:
    종목.append(stock.get_market_ticker_name(i))

print(종목)


df = stock.get_market_ohlcv_by_date("20180810", "20181212", "005930")
print(df.head(3))
df = stock.get_market_ohlcv_by_date("20180810", "20181212", "005930", "m")
print(df.head(3))

# 1초에 한 번 씩 모든 종목 ohlcv 가져오기
import time
for ticker in stock.get_stock_ticker_list():
    df = stock.get_market_ohlcv_by_date("20181210", "20181212", ticker)
    print(df.head())
    time.sleep(1)

# 모든 종목의 가격 변동 조회
df = stock.get_market_price_change_by_ticker("20180301", "20180320")
print(df.head(2))


# 종목별 DIV/BPS/PER/EPS 조회
df = stock.get_market_fundamental_by_ticker("20180305")
print(df.head(2))


# 일자별 DIV/BPS/PER/EPS 조회
df = stock.get_market_fundamental_by_date("20180301", "20180320", '005930')
print(df.head(2))

df = stock.get_market_fundamental_by_date("20180810", "20181212", "005930", "m")
print(df.head(2))

# 특정종목 일자별 시가총액 조회

df = stock.get_market_cap_by_date("20190101", "20190131", "005930")
print(df.head())
df = stock.get_market_cap_by_date("20200101", "20200430", "005930", "m")
print(df.head())


# 특정종목 일자별 공매도 거래현황
df = df = stock.get_shorting_volume_by_date("20200101", "20200115", "005930")
print(df.head())