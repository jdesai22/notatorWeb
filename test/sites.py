import requests
from bs4 import BeautifulSoup as bs


def getArticle(get_url):
    webpage = requests.get(get_url)
    webInfo = bs(webpage.text, 'html.parser')

    results = webInfo.find_all('div', attrs={'class': 'article-body'})

    p = results[0].find_all('p', attrs={'class': None})
    mainArticle = []

    # for i in p:
    #     mainArticle.append(i.get_text())

    for i in p:
        mainArticle.append(i)


    print(mainArticle)

if __name__== "__main__":
    # url = str(input("url: "))

    url = "https://www.foxnews.com/politics/geraldo-rivera-trump-election-results-white-house"
    getArticle(url)
