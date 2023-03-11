import requests
from bs4 import BeautifulSoup as soup
import random
import sqlite3

from deep_translator import GoogleTranslator


search = "" # keywords to be searched in science journals.
translateTo = "" # language to be translated to (Example - en).



url = "https://www.nature.com/search?q=" + search + f"&page={i}"







db = sqlite3.connect("Journals.db")
cur = db.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS Journals (
    ID INTEGER PRIMARY KEY,
    NAME_OF_THE_ARTICLE TEXT,
    NAME_OF_THE_ARTICLE_TRANSLATED TEXT,
    NAME_OF_THE_SECTION TEXT,
    NAME_OF_THE_SECTION_TRANSLATED TEXT,
    P_TEXT TEXT,
    P_TEXT_TRANSLATED TEXT,
    LINK_TEXT TEXT
    )""")
db.commit()

user_agent_list = [
"Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0",
"Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0",
"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41",
"Opera/9.80 (Macintosh; Intel Mac OS X; U; en) Presto/2.2.15 Version/10.00",
"Opera/9.60 (Windows NT 6.0; U; en) Presto/2.1.1",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59",
]

user_agent = random.choice(user_agent_list)

header = {"User-Agent" : user_agent}

translator = GoogleTranslator(source = 'en', target = translateTo)


for i in range(1,5):
    
    pageOfPages = soup(requests.get(url, headers = header).text, "lxml")



    # links
    links = []
    for article in pageOfPages.find_all("a", class_="u-link-inherit"):
        link = "https://www.nature.com"+article.get("href")
        links.append(link)




counter = 1
for link in links:
    page = soup(requests.get(link, headers = header).text, "lxml")
    article_title = page.find("h1", class_="c-article-title").text
    article_title_translated = translator.translate(article_title)
    for section in page.find_all("section"):
        try:
            if section["data-title"] == "References" or section["data-title"] == "References:" or section["data-title"] == "Reference":
                break
            else:
                print(f"Title: {article_title}")
                for p_element in section.find_all("p"):
                    p_text = p_element.text
                    translated = translator.translate(p_text)
                    cur.execute("""INSERT INTO Journals (NAME_OF_THE_ARTICLE, NAME_OF_THE_ARTICLE_TRANSLATED, NAME_OF_THE_SECTION, NAME_OF_THE_SECTION_TRANSLATED, P_TEXT, P_TEXT_TRANSLATED, LINK_TEXT) VALUES (?, ?, ?, ?, ?, ?, ?);""", (article_title, article_title_translated, section["data-title"], translator.translate(section["data-title"]), p_text, translated, link))
                    db.commit()
                    print(f"ADDED {counter}")
                    counter = counter + 1
        except KeyError:
            continue
        except:
            f = open("Translator Exceptions.txt", "at")
            f.write(f"{article_title} \n\n{article_title_translated} \n\n{section['data-title']} \n\n{translator.translate(section['data-title'])} \n\n{p_text} \n\n{link} \n\n_________________________________________________")
            f.close()


