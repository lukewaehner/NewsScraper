from bs4 import BeautifulSoup
import requests

symbol = input("Enter a NYSE stock ticker: ")
url = "https://seekingalpha.com/symbol/" + symbol + "/news"
response = requests.get(url)

if response.status_code == 200:
    html = response.text
else:
    print("Failed to retrieve the page from:" + url)


soup = BeautifulSoup(html, 'html.parser')

# find and extract the articles -> from link with class jf_G (idk why class named this)

news_articles = soup.find_all(
    'article', class_='gC_gX fN_gX r_4 s_aQ s_bd kX_JD s_aE s_bH kX_JD s_aE s_bH kX_JH kX_JH gC_z5')

for article in news_articles:
    link_element = article.find('a', href=True)
    if link_element:
        url = link_element['href']
        title = link_element.text.strip()
        print("Title:", title)
        print("URL:", "https://seekingalpha.com/" + url, "\n")
    else:
        print("URL not found")
