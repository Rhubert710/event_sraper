import sqlite3
import csv
from bs4 import BeautifulSoup
import requests
import pandas as pd


def update_url(url):
    # Getting the html file and parsing with html.parser
    html = requests.get(url)
    bs = BeautifulSoup(html.text, 'html.parser')
    print(url)
    return bs



bs = update_url('https://www.xda-developers.com/')

# def write_csv():

#     with open('xda_data.csv', 'w') as xda_csv:
#         line_writer = csv.writer(xda_csv)

#     global headlines
#     for i in range(len(headlines)):
        
#         line_writer.writerow([headlines[i], excerpts[i], authors[i], dates[i]])
    

# def create_csv(file_name):
# csv_file = open('xda_data.csv', 'w')
# dictwriter = csv.DictWriter(csv_file, fieldnames=['Headline', 'Excerpt', 'Author', 'Date_Posted'])
# dictwriter.writeheader()
# create_csv('xda_data.csv')

# number_of_pages_to_scrape = 4  # limits number of pages

df = pd.DataFrame(columns = ['Headline', 'Excerpt', 'Author', 'Date_Posted'])

def scrape_page():
    headlines = []
    excerpts = []
    authors = []
    dates = []

    for article in bs.find_all('div', class_="row latest-news-2"):

        for headline in article.find_all('h4'):

            headlines.append(str(headline.text).replace(',', ' '))

        for excerpt in article.find_all('div', class_='the-excerpt'):

            excerpt_str = str(excerpt.text)
            excerpts.append(excerpt_str.replace(',', ''))

        for author in article.find_all('span', class_='meta_author'):

            authors.append(author.text)

        for date in article.find_all('span', class_='meta_date'):

            dates.append(date.text)


    # writes data into csv
    if len(headlines) == len(excerpts) == len(authors) == len(dates):

        with open('xda_data.csv', 'a', newline='') as xda_csv:
            line_writer = csv.writer(xda_csv)

            for i in range(len(headlines)):
        
                line_writer.writerow([headlines[i], excerpts[i], authors[i], dates[i]])

        # def write_to_df():
            # print(headlines)
            # global df
        # for i in range(len(headlines)):
            # global df
            # df = df.append({'Headline': headlines[i], 'Excerpt': excerpts[i], 'Author': authors[i], 'Date_Posted': dates[i]}, ignore_index=True)
pages = 6
for page in range(1,pages+1):
 
    scrape_page()

    bs = update_url(bs.find('a', class_='next page-numbers')['href'])

# df.to_csv('xda_data.csv', index=False)


# def write_csv():

#     print(df)
    # df.to_csv('xda_data.csv', index=False)

# write_csv()

    
    #condiotion: number of pages to scrape before break
    # number_of_pages_to_scrape -= 1
    # if number_of_pages_to_scrape == 0:
            
    #     break

# except:
#     print('Unknown Error!!!')
# finally:

# conn = sqlite3.connect('xda_data.db')
# c = conn.cursor()
# c.execute('''CREATE TABLE xda_data (Headline text, Excerpt text, Author text, Date_posted text)''')


# xda_df = pd.read_csv('xda_data.csv', delim_whitespace=True)
# xda_df.to_sql('xda_data', conn, if_exists='append', index = False)

# a = c.execute('''SELECT * FROM xda_data''').fetchall()

# print(a)

# csv_file.close()
