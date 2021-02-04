import numpy as np
#import Counter as counter
from collections import Counter
import requests
from bs4 import BeautifulSoup as bs


def convert(arr):
    res = []
    for i in arr:
        res.append(i.encode("ascii", "ignore"))
    return res


def convert2(arr):
    asc = []
    count = 0
    for i in arr:
        res = []
        for s in range(0, len(i)):
            inter = arr[count][s]
            res.append(inter.encode("ascii", "ignore"))
        asc.append(res)
        count += 1
    return asc


def createNotes(source, get_url, webType, txt, kw):
    # source = str(input("[u]rl or [c]opy and paste: "))

    if source == "u":
        # get_url = str(input("Link to webpage: "))
        # webType = str(input("[n]ew york times or [w]ashington post or new [y]ork post: "))

        webpage = requests.get(get_url)
        webInfo = bs(webpage.text, 'html.parser')

        if webType == "nTimes":
            # results = webInfo.find_all('p', attrs={'class': 'css-158dogj'}) #NEW YORK TIMES css-1g7m0tk
            results = webInfo.find_all('p', attrs={'class': 'css-axufdj'})
        elif webType == "wPost":
            results = webInfo.find_all('p', attrs={'class': 'font--body'}) #WASHINGTON POST
        elif webType == "nPost":
            results = webInfo.find_all('div', attrs={'class': 'entry-content'}) #NEW YORK POST
        elif webType == "fox":
            results = webInfo.find_all('div', attrs={'class': 'article-body'})
            results = results[0].find_all('p', attrs={'class': None})
        elif webType == "chicago":
            interResults = webInfo.find_all('div', class_="crd clln--it")
            results = []
            for i in interResults:
                results.append(i)

        mainArticle = []
        for i in results:
            mainArticle.append(i.text)

    elif source == "c":
        # file = open("article.txt", "r", encoding="utf8")
        # mainArticle = file.readlines()
        mainArticle = []
        # print(txt)
        for i in txt.split(" "):
            mainArticle.append(i)


    lineCount = 0
    wordCount = 0
    charCount = 0
    highestWordCount = 0
    rowWithMostWords = 0
    wordsInRow = 0
    k = 0

    for i in mainArticle:
        #REMOVE LINE BREAKS FROM END OF EACH LINE
        i = i.rstrip("\n")
        mainArticle[k]=i
        # k+=1

        #CREATE ARRAY OF ALL WORDS IN EACH LINE
        words = i.split()

        #GET FILE INFORMATION
        lineCount+=1
        wordCount+=len(words)
        charCount += len(i) #INCLUDES SPACES

        #SET ROW WITH HIGHEST WORD COUNT
        wordsInRow = len(words)
        if wordsInRow > highestWordCount:
            highestWordCount = wordsInRow
            rowWithMostWords = k

        k += 1

    #DEFINE 2D ARRAY WITH ALL WORDS IN EACH LINE
    rows, cols = (k, highestWordCount)
    articleWords = []
    t = 0

    for i in range(rows):
        rowWords = mainArticle[i]
        rowWords = rowWords.split()
        #adding extra value so each row has same number of items
        t = len(rowWords)
        if t != cols:
            for i in range(cols-t):
                rowWords.append("null")

        articleWords.append(rowWords)


    #FINDING MOST USED WORDS AKA KEYWORDS
    #FLATTEN ARRAY INTO 1D ARRAY
    oneDArticle = np.array(articleWords)
    oneDArticle = oneDArticle.flatten()
    allQuote = oneDArticle.tolist() #FOR LATER WHEN FINDING THE QUOTATIONS WITHIN TEXT

    #REMOVING PUNCTUATION
    noPunctuation = np.array([])
    l = 0
    for o in oneDArticle:
        #inter = list(i)
        #inter = np.array(inter)
        #inter = [i for i in inter if 47 < ord(i) < 58 or 64 < ord(i) < 91 or 96 < ord(i) < 123]
        #inter = "".join(inter)
        inter = "".join([i for i in np.array(list(o)) if 47 < ord(i) < 58 or 64 < ord(i) < 91 or 96 < ord(i) < 123]) #COMBINE THE 4 LINES ABOVE INTO ONE
        noPunctuation = np.append(noPunctuation, inter)
        l+=1

    oneDArticle = noPunctuation

    #REMOVE VERY COMMON AND IRRELEVANT WORDS
    #read banned.txt
    # file = open("/Users/jaidesai/PycharmProjects/notatorWeb/static/text/banned.txt", "r")
    # file = open("/utils/banned.txt", "r")
    file = open("utils/banned.txt", "r")
    bannedWords = file.readlines()
    l = 0
    for i in bannedWords:
        i = i.rstrip("\n")
        bannedWords[l] = i
        l+=1

    oneDArticle = [i for i in oneDArticle if i.lower() not in bannedWords] #FILTERING OUT BANNED WORDS


    #USE COUNTER CLASS TO FIND MOST COMMON WORDS IN THE ARTICLE
    numberOfKeywords = int(kw)
    counterArticle = Counter(oneDArticle)
    mostCommon = counterArticle.most_common(numberOfKeywords)
    mostCommon = np.array(mostCommon)

    #DISPLAY INFO SUCCINCTLY
    keywords = mostCommon[:, 0]
    # newKey = []

    # for i in keywords:
    #     newKey.append(i)
    #
    # keywords = newKey

    #SPLITTING ARTICLE INTO SENTENCES need to fix at mr mrs and ms so it doesnt read as diff sentences
    sentences = [i for i in allQuote if i not in 'null']
    newSentences = []
    #PLACING MARKER /// BETWEEN SENTENCES
    for i in sentences:
        letters = list(i)
        endOfSentence = False
        lenLetters = len(letters)
        for k in range(0, lenLetters):
            if letters[k] == '.':
                try:
                    prev1 = "".join([letters[k - 2], letters[k - 1]])
                    prev2 = "".join([letters[k - 3], letters[k - 2], letters[k - 1]])
                    if prev1 == 'Mr' or prev1 == 'Dr':
                        endOfSentence = False
                    elif prev2 == 'Mrs':
                        endOfSentence = False
                    else:
                        endOfSentence = True
                except:
                    endOfSentence = True
        letters = "".join(letters)
        newSentences.append(letters)
        if endOfSentence:
            newSentences.append("///")

    sentences = newSentences
    sentences2d = []
    l=0
    lastEnd = 0
    #USING MARKER TO SPLIT MAKE EACH ROW A SENTENCE IN 2D ARRAY
    for i in sentences:
        rowSent = []
        if i == "///":
            for q in sentences[lastEnd: l]:
                rowSent.append(q)
            rowSent = [i for i in rowSent if i not in '///']
            sentences2d.append(rowSent)
            lastEnd = l
        l+=1

    #FIND WHICH SENTENCES CONTAIN WHICH KEYWORDS
    keywordsLoc = []
    for i in keywords:
        tempKeywordloc = []
        l = 0
        for s in sentences2d:
            inSentence = False
            for w in s:
                w = list(w)
                w = [q for q in w if q not in [',', '.', '"', "!", "?", "'"]] #QUICK REMOVAL OF PUNCTUATION
                w = "".join(w)
                if i == w:
                    inSentence = True
                    break #EXIT IMMEDIATELY AFTER KEYWORD APPEARS
            if inSentence:
                tempKeywordloc.append(l) #RECORD SENTENCE LOCATION
            l+=1
        keywordsLoc.append(tempKeywordloc)

    #OUTPUT THE NOTES - CORNELL STYLE
    # print("\n\n Notes from Today: \n\n")
    notes = []
    for i in range(0, numberOfKeywords):
        # print(keywords[i] + "\n")
        tempNotes = []
        for l in keywordsLoc[i]:
            cleanNotes = []
            badCharacters = [39]
            for m in sentences2d[l]:
                cleanWord = []
                for s in list(m):
                    if 43 < ord(s) < 60 or ord(s) == 63 or 64 < ord(s) < 94 or 96 < ord(s) < 123:
                        cleanWord.append(s)

                cleanNotes.append("".join(cleanWord))

            fullNotes = " ".join(cleanNotes)

            tempNotes.append(fullNotes)

        notes.append(tempNotes)

            # print("\n")

        # print("-----------------------")
        # print("\n")


    #GET ALL QUOTATIONS WITHIN THE ARTICLE
    allQuote = [i for i in allQuote if i not in 'null']
    allQuote = ' '.join(allQuote)
    allQuote = list(allQuote)
    l = 0
    indexQuote = []
    quotes = []

    #RECORDING WHERE QUOTATION MARKS ARE
    for i in allQuote:
        if i == '"' or ord(i) == 8220 or ord(i) == 8221 or ord(i) == 8223: #or i =="'" APOSTROPHES CAN BE ADDED BUT CONFUSING BECAUSE OF WORDS LIKE WON'T, ETC.
            indexQuote.append(l)
        l+=1

    #GETTING INFO BETWEEN THE RECORDED LOCATIONS OF QUOTATION MARKS
    for i in range(0, int(len(indexQuote)/2)):
        interQuote = []

        for s in allQuote[indexQuote[i*2]:indexQuote[(2*i)+1]+1]:#ADDITIONAL OPERATIONS SO THAT IT GOES TO APPROPRIATE QUOTATIONS
            # encode it so it displays on webpage
            interQuote.append(s)

        quotes.append("".join(interQuote))


    kw = convert(keywords)
    note = convert2(notes)
    quote = convert(quotes)
    return [kw, note, quote]
    # return [keywords, notes, quotes]


