from bs4 import BeautifulSoup
import requests
URL = "https://kusom.edu.np/index1.php?option=WJDIpLoIs5QpJwuXGc2d1G8y3opIAmHGWWDq_Y1zXIQ"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
all_news = soup.find_all('div', id="news-block")
for news in all_news:
    # print(news)
    news_title = news.find("h4").find('a').text
    news_url = news.find("h4").find("a").get("href")
    publish_date = news.find("span",class_="date").text

    print(news_title, news_url, publish_date)

# Get news from all pages??