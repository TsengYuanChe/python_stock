import requests
from bs4 import BeautifulSoup
def stock_price(stock:str):
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    data = requests.get(f"https://finance.yahoo.com/quote/{stock}?.tsrc=fin-srch",headers=headers)
    soup = BeautifulSoup(data.text,features="lxml")
    price = soup.find("fin-streamer",{"data-test": "qsp-price"})
    return price.text