#ライブラリのインポート
from pandas_datareader.stooq import StooqDailyReader
import datetime as dt
import bottleneck as bn
import japanize_matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import streamlit as st

# ma は moving averageの略。

#株価取得範囲を設定
start = dt.datetime(int(dt.datetime.now().strftime('%Y')) - 4, 1, 1)
end = dt.datetime.now()
#銘柄コードを入力
#日経平均株価とTopix
stock = ['^NKX','^DJI','^TPX']

#株価取得
df = StooqDailyReader(stock, start=start, end=end)
df_stock = df.read()['Close']

df_stock = df_stock.fillna(method='ffill')
for column in df_stock:
  df_stock[df_stock[column].name + '_3days_ma'] = bn.move_mean(df_stock[column], window=3)

# print(df_stock.head(15)) 
# print(df_stock.tail(15))

#matplotlibで株価をグラフ化
fig = plt.figure()

ax1 = fig.add_subplot()
ax2 = ax1.twinx()
ax1.plot(df_stock.index,
         df_stock['^DJI_3days_ma'], color="orange", label='NYダウ(^DJI)')
ax1.plot(df_stock.index,
         df_stock['^NKX_3days_ma'], color="blue", label='日経225(^NKX)')
ax2.plot(df_stock.index,
         df_stock['^TPX_3days_ma'], color="green", label='TOPIX(^TPX)')
locator = mdates.MonthLocator(bymonthday=15, interval=2)
ax1.xaxis.set_major_locator(locator)
ax1.xaxis.set_tick_params(rotation=45)

ax1.set_ylabel("NYダウ/日経225")  # y1軸ラベル
ax2.set_ylabel("TOPIX")  # y2軸ラベル

# 凡例
h1, l1 = ax1.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
ax1.legend(h1+h2, l1+l2, loc='lower right')
# plt.show()


# streamlitで表示
st.pyplot(fig)
st.subheader('直近5日間の終値')
st.dataframe(df_stock.loc[:,['^DJI','^NKX','^TPX']].tail(5))
