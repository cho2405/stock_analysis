import FinanceDataReader as fdr
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta



df = fdr.DataReader('003240', '2018')


ma_ls = [20,30,60]
for i in range(len(ma_ls)):
    a = df['Close'].rolling(window=ma_ls[i]).mean()
    df['MA'+str(ma_ls[i])] = a
print(df)


df.dropna(inplace=True, axis=0) #데이터 결측치 제거
delta = datetime(2018, 4, 1) - datetime(2018, 1, 1)

date_index = abs(df['MA20']-df['MA60']).sort_values().head(5).index
#해당 주식의 20일 이동평균과 60일 이동평균을 이용하여 구한 최적의 매매시점은 다음과 같다.(date_index)
#여기서 반환해주는 날짜는 + - 1일을 기준으로 ma20과 ma60이 교차하는 날짜인 즉, cross 날짜가 된다.
print(date_index)


def MA_backtesting(month):  # 몇개월을 생각하고 주식을 매수하고 매도할 것인지 parameter

    if month == 3:  # 3개월의 날짜를 구한 것
        delta = datetime(2018, 4, 1) - datetime(2018, 1, 1)
    elif month == 6:  # 6개월의 날짜를 구한 것
        delta = datetime(2018, 6, 30) - datetime(2018, 1, 1)
    else:  # 9개월의 날짜를 구한 것
        delta = datetime(2018, 9, 28) - datetime(2018, 1, 1)

    revenue = pd.DataFrame({'date': [],
                            'revenue': []})
    for i in range(len(date_index)):

        # 3개월/6개월/9개월만큼의 수익률을 구하는 과정에서 만일 3개월/6개월/9개월 뒤의 날짜가 공휴일
        # 이거나 주말이여서 주식시장이 오픈을 하지 않는 것을 대비해서 무조건 산출할 수 있는 예를들어
        # 금요일이면 +3일 - 월요일 / 토요일이면 +2일 - 월요일 /일요일이면 +1일 - 월요일
        # 로 봤을 때 +3일까지의 대비변수를 마련해 놓으면 따로 예외처리하지 않고도 무조건
        # 결과를 도출할 수 있다.
        day1 = datetime(2018, 1, 2) - datetime(2018, 1, 1)  # 예비1일
        day2 = datetime(2018, 1, 3) - datetime(2018, 1, 1)  # 예비2일
        day3 = datetime(2018, 1, 4) - datetime(2018, 1, 1)  # 예비3일

        # 예외처리로 1일~3일까지 더할 수 있는 코드를 짜서 Error를 피한다.
        try:
            a = df.loc[date_index[i] + delta, 'Close']
        except:
            try:
                a = df.loc[date_index[i] + delta + day1, 'Close']
            except:
                try:
                    a = df.loc[date_index[i] + delta + day2, 'Close']
                except:
                    a = df.loc[date_index[i] + delta + day3, 'Close']

        # a = date_index 즉, 접하는 지점으로부터 알고리즘 사용자가 지정한 날을 더한 날짜의 종가를 구한다

        b = df.loc[date_index[i], 'Close']  # date_index의 날짜의 종가데이터를 추출
        revenue0 = a / b  # 수익률 및 손실률
        insert_data = pd.DataFrame({'date': [date_index[i]],
                                    'revenue': [revenue0]})

        revenue = revenue.append(insert_data)

    revenue.index = range(len(revenue))

    acc_date0 = revenue.sort_values('revenue', ascending=False)['date'].iloc[0]  # 최대 수익률의 날짜
    acc_date00 = revenue.sort_values('revenue', ascending=False)['date'].iloc[len(revenue) - 1]  # 최대 손실률의 날짜

    try:
        a_df = df.loc[acc_date0:acc_date0 + delta, 'Close']
    except:
        try:
            a_df = df.loc[acc_date0:acc_date0 + delta + day1, 'Close']
        except:
            try:
                a_df = df.loc[acc_date0:acc_date0 + delta + day2, 'Close']
            except:
                a_df = df.loc[acc_date0:acc_date0 + delta + day3, 'Close']
    # a_df = 최대이익이 날 수 있는 접점날짜부터 알고리즘 사용자가 정한 날까지의 종가 데이터

    try:
        b_df = df.loc[acc_date00:acc_date00 + delta, 'Close']
    except:
        try:
            b_df = df.loc[acc_date00:acc_date00 + delta + day1, 'Close']
        except:
            try:
                b_df = df.loc[acc_date00:acc_date00 + delta + day2, 'Close']
            except:
                b_df = df.loc[acc_date00:acc_date00 + delta + day3, 'Close']

    # b_df = 최대손실이 날 수 있는 접점날짜부터 알고리즘 사용자가 정한 날까지의 종가 데이터
    print(a_df)
    print(b_df)
    plt.subplot(121)
    a_df.index = a_df.index.strftime("%Y-%m-%d")
    a_df.plot(figsize=(15, 8))  # 이익률 그래프

    print(a_df.index)

    plt.subplot(122)
    b_df.index = b_df.index.strftime("%Y-%m-%d")
    b_df.plot(figsize=(15, 8), c='b')  # 손실률 그래프

    acc_date = str(revenue.sort_values('revenue', ascending=False)['date'].iloc[0])
    acc_revenue = str(revenue.sort_values('revenue', ascending=False)['revenue'].iloc[0])

    acc_date2 = str(revenue.sort_values('revenue', ascending=False)['date'].iloc[len(revenue) - 1])
    acc_revenue2 = str(revenue.sort_values('revenue', ascending=False)['revenue'].iloc[len(revenue) - 1])

    print('Golden Cross')
    print('이동평균선을 이용하여 고객님에게 맞는 최적의 매수시점은 ' + acc_date + '입니다.')
    print('이동평균선을 이용하여 최적의 매수시점에 주식을 매수하고 ' + str(month) + '개월 뒤에 매도했을 때' + acc_revenue + '배의 수익을 얻을 수 있습니다.\n\n\n')

    print('Bad Cross')
    print('이동평균선을 이용하여 고객님에게 맞는 최적의 매도시점은 ' + acc_date2 + '입니다.')
    print('이동평균선을 이용하여 최적의 매도시점에 주식을 매도하지않으면 ' + str(month) + '개월 뒤에 매도했을 때' + acc_revenue2 + '배의 손실을 얻을 수 있습니다.')

    plt.tight_layout()
    plt.show()
    return revenue.sort_values('revenue', ascending=False)


MA_backtesting(3)