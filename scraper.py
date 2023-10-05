from bs4 import BeautifulSoup
import requests
import re


def Scrape(symbol):

    urls = {"Yahoo Finance": "https://finance.yahoo.com/quote/" + symbol + "?p=" + symbol + "&.tsrc=fin-srch",
            "Seeking Alpha": "https://seekingalpha.com/symbol/" + symbol + "/news",
            "Market Watch": "https://www.marketwatch.com/investing/stock/" + symbol + "?mod=search_symbol"
            }
    articles = {}  # dict key -> title, value -> url
    linksYF = linksSA = 0
    for search in urls:
        response = requests.get(urls[search])

        if response.status_code == 200:
            html = response.text
        else:
            print("Failed to retrieve the page from:" + search)

        soup = BeautifulSoup(html, 'html.parser')

        if search == "Seeking Alpha":
            news_articles = soup.find(
                'div', attrs={"data-test-id": "post-list"})
        elif search == "Yahoo Finance":
            news_articles = soup.find(
                'div', id="quoteNewsStream-0-Stream")
        elif search == "Market Watch":
            filter_source = soup.find_all(
                'mw-tabs')
            if len(filter_source) >= 2:
                news_articles = filter_source[1]

        link_element = news_articles.find_all('a', href=True)

        for links in link_element:
            url = links.get('href')
            title = links.text.strip()
            if search == "Yahoo Finance":
                if (linksYF < 5 and len(articles) < len(urls)*5):
                    articles[title] = "https://finance.yahoo.com/" + url
                    linksYF += 1
            elif search == "Seeking Alpha":
                if (linksSA < 5 and len(articles) < len(urls)*5):
                    if 'comments' and 'comment' not in links.get_text().lower():
                        articles[title] = "https://seekingalpha.com/" + url
                        linksSA += 1
            elif search == "Market Watch":
                if (len(articles) < len(urls)*5):
                    articles[title] = url

    unique_articles = {}

    # Iterate through the original dictionary and add unique keys and values to the new dictionary
    for key, value in articles.items():
        if key not in unique_articles:
            unique_articles[key] = value

    for key, value in unique_articles.items():
        print(key + ":")
        print(value)
        print()


symbol = input("Enter a NYSE stock ticker: ")
Scrape(symbol)
