import sqlite3
import time

search = input("Enter the key words: ")



print("Processing request...")


db = sqlite3.connect("Journals.db")
cur = db.cursor()

counter = 0

for text in cur.execute('SELECT ID NAME_OF_THE_ARTICLE_TRANSLATED, NAME_OF_THE_SECTION_TRANSLATED, P_TEXT_TRANSLATED, P_TEXT, LINK_TEXT FROM Journals WHERE P_TEXT_TRANSLATED LIKE ?', ('%' + search + '%',)):
    print("________________")
    for result in text:
        print(result, end = "\n \n")
    counter = counter + 1
print(f"Total - {counter}.")
