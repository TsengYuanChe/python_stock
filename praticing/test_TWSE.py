import TWSE as tw
date = "20210225"
data = tw.twes_data(f"{date}")
print(data)