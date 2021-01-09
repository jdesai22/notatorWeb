import requests
from bs4 import BeautifulSoup as bs


def getArticle(get_url):
    webpage = requests.get(get_url)
    webInfo = bs(webpage.text, 'html.parser')

    results = webInfo.find_all('div', attrs={'class': 'article-body'})
    results = results[0].find_all('p', attrs={'class': None})
    print(results)
    # # for i in p:
    # #     mainArticle.append(i.get_text())
    #
    # for i in p:
    #     mainArticle.append(i)
    #
    #
    # print(mainArticle)

def chicage(url):
#      crd--cnt
    webpage = requests.get(url)
    webInfo = bs(webpage.text, 'html.parser')
    # print(webInfo)
    results = webInfo.find_all('div', class_="crd clln--it")
    # results = results[0].find_all('p', attrs={'class': None})
    article = bs
    # print(results)
    for i in results:
        article.append(i.find('p', class_=""))

    for i in article:
        print(i.text)


    # print(article)


# //*[@id="f9NVCJ1LNOXhhs"]/div[2]
def nyTime(url):
    r = requests.get(url)
    info = bs(r.text, 'html.parser')

    res = info.find_all('p', attrs={'class': 'css-axufdj'})
    # css-axufdj evys1bk0
    print(res)

if __name__== "__main__":
    # url = str(input("url: "))

    # url = "https://www.foxnews.com/politics/geraldo-rivera-trump-election-results-white-house"
    # getArticle(url)

    chicage('https://www.chicagotribune.com/coronavirus/ct-nw-second-stimulus-check-updates-20201227-lcuwnmemifapxht4f7jcltmjmi-story.html')

    # nyTime('https://www.nytimes.com/2020/12/26/us/explosion-nashville-rv.html?action=click&module=Top%20Stories&pgtype=Homepage')
