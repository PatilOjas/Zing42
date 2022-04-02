import pandas as pd
import datetime

# today = datetime.datetime.now().date()
# dates = pd.date_range(today-datetime.timedelta(days=30), today, freq='D')
# for d in dates:
# 	date = str(d.strftime("%d")) + str(d.strftime("%b")).upper() + str(d.strftime("%Y"))
# 	year = str(d.strftime("%Y"))
# 	month = str(d.strftime("%b")).upper()
# 	print(date, str(d.strftime("%A")))
# 	if str(d.strftime("%A")) not in ['Saturday', 'Sunday']:
# 		df = pd.read_csv(f"https://archives.nseindia.com/content/historical/EQUITIES/{year}/{month}/cm{date}bhav.csv.zip")
# 		print(df['SYMBOL'])

df = pd.read_csv("https://archives.nseindia.com/content/historical/EQUITIES/2022/APR/cm01APR2022bhav.csv.zip")
print(df[df.columns[:-1]].columns)
