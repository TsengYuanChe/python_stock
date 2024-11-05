import requests
from bs4 import BeautifulSoup
import pandas as pd
def get_yahoo_news(stock: str):
    headers = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
    data = requests.get(f"https://tw.stock.yahoo.com/quote/{stock}/news",headers=headers)
    soup = BeautifulSoup(data.text,"html.parser")
    all_news = soup.find_all("h3",{"class":"Mt(0) Mb(8px)"})
    all_news_store = []
    for a in all_news:
        news_path = a.find("a")["href"]
        if news_path[-4:] == "html":
            all_news_store.append(news_path)

    date_store, title_store = [], []
    for new in all_news_store:
        each_data = requests.get(f"{new}", headers=headers)
        each_soup = BeautifulSoup(each_data.text,"html.parser")
        title = each_soup.find("h1",{"data-test-locator": "headline"}).text
        news_time = each_soup.find("div",{"class":"caas-attr-time-style"}).text
        news_time = news_time.split(" ")[0]
        news_time = news_time.replace("年","/")
        news_time = news_time.replace("月","/")
        news_time = news_time.replace("日","")
        title_store.append(title)
        date_store.append(news_time)
    result = pd.DataFrame()
    result["title"] = title_store
    result["date"] = date_store
    result["url"] = all_news_store
    return result
        