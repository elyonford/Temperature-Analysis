import pandas as pd
import matplotlib.pyplot as plt

kansas_city = pd.read_csv("data/USW00003947.csv")
kansas_city["Date"] = pd.to_datetime(kansas_city["Date"]) #Thanks skbrimmer!
print(kansas_city.describe())

kc_lows = kansas_city[["Date","tmin"]]
# kc_lows_since1970 = kc_lows[kc_lows["Date"] > "1969-12-31"]
kc_lows_since2010 = kc_lows[kc_lows["Date"] > "2009-12-31"]
 
print(kc_lows_since2010)
# print(kc_lows_since2010.info())
 
# kc_lows_since2010.plot(x="Date")
# plt.savefig("low_temperatures.png")
# plt.show()