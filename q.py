import csv
from bs4 import BeautifulSoup
import requests

# URL to the website
URL = 'http://quotes.toscrape.com/tableful/'

# Getting the html file and parsing with html.parser
html = requests.get(URL)
bs = BeautifulSoup(html.text, 'html.parser')

# Tries to open the file
try:
    csv_file = open('quote_list.csv', 'w')
    fieldnames = ['quote', 'author', 'tags']
    dictwriter = csv.DictWriter(csv_file, fieldnames=fieldnames)

    # Writes the headers
    dictwriter.writeheader()

    # While next button is found in the page the loop runs
    while True:
        # Loops through quote in the page
        for td in bs.find_all('td'):
            # Extract the text part of quote, author and tags
           ## text = quote.find('span', {'class': 'text'}).text
            ##author = quote.find('small', {'class': 'author'}).text
            ##tags = []
            ##for tag in quote.findAll('a', {'class': 'tag'}):
                ##tags.append(tag.text)
            # Writes the current quote,author and tags to a csv file
            ##dictwriter.writerow(
                ##{'quote': text, 'author': author, 'tags': tags})
            if len(td.contents) != 0:
                if '“' in td.contents[0]:
                    line = td.contents[0].split('”')
                    #line : ["quote", autor:authorsName]
                    quote = line[0]
                    author = line[1].split(':')[1]
                    dictwriter.writerow({'quote': quote, 'author': author})

                if 'Tags' in td.contents[0]:
                    tags =[]

                    for tag in td.contents:
                        if type(tag) == type(td.contents[1]):
                            tags.append(tag.contents)
                    dictwriter.writerow({'tags': tags})





            
            print(td.contents)
            print('oooooooooooo')

        # Finds the link to next page
        next = bs.find('li', {'class': 'next'})
        if not next:
            break

        # Gets and parses the html file of next page
        html = requests.get(URL+next.a.attrs['href'])
        bs = BeautifulSoup(html.text, 'html.parser')
except:
    print('Unknown Error!!!')
finally:
    csv_file.close()