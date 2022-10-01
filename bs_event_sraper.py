import sqlite3
import csv

from bs4 import BeautifulSoup
import requests
import pandas as pd
import json
import copy






#functions#
def bsParser(url):
    # Getting the html file and parsing with html.parser
    html = requests.get(url)
    bs = BeautifulSoup(html.text, 'html.parser')
    return bs

#variables#
page = 1

DATE = f'2022-10-01'
DATE_TEXT = f'Oct {1}'

individual_event_hrefs = []
picture_list = []
profile_pictue_list = []
data_on_page = True



'''
main
'''
soup = bsParser(f'https://www.eventbrite.com/d/ny--new-york/all-events/?end_date={DATE}&page={page}&start_date={DATE}')


# while(data_on_page):/
while(page<=1):


    # base case to end loop
    end = soup.find_all("section", class_="empty-state")
    if end:
        print('Done sdraping pages')
        break

    ## GET INDIVIDUAL EVENT HREFS ##

    events_on_current_page = soup.find_all('div', class_='search-event-card-square-image')

    for event in events_on_current_page:

        date_on_card = event.find('div', class_='eds-event-card-content__sub-title eds-text-color--primary-brand eds-l-pad-bot-1 eds-l-pad-top-2 eds-text-weight--heavy eds-text-bm')
        if(DATE_TEXT in date_on_card.text):

            new_href = event.find('a', class_='eds-event-card-content__action-link')
            individual_event_hrefs.append(new_href['href'])

    # print and increment
    print(f'page scraped: {page}')

    page+=1
    soup = bsParser(f'https://www.eventbrite.com/d/ny--new-york/all-events/?end_date={DATE}-28&page={page}&start_date={DATE}')


'''
Going through each individual article
'''
total_articles = len(individual_event_hrefs)
print(total_articles)
#loop
for i, article_url in enumerate(individual_event_hrefs, 1):

    soup = bsParser(article_url)

    new_obj ={}
    new_porfile_pic_obj = {}


    # get profile pic
    try:

        profile_pic = soup.find('img', class_='listing-image--main')
        new_porfile_pic_obj['src'] = profile_pic['src']
    
    except:
        try:

            profile_pic_container = soup.find('picture')
            profile_pic = profile_pic_container.find('img')

            new_porfile_pic_obj['src'] = profile_pic['src']

        except:
            new_porfile_pic_obj['src'] = 'NOPIC'

    
    new_obj['url'] = article_url
    new_porfile_pic_obj['url'] = article_url


    # get address info
    try:
        location_h2_element = soup.find(id="location-heading")
        address_p_tags = location_h2_element.parent.parent.find_all('p')

        address = f'{address_p_tags[1].string} {address_p_tags[2].string}'
    except:
        address = 'NONE'

    # determine boro

    boro = 'NONE'
    if 'brooklyn' in address.lower():
        boro = 'brooklyn'
    if 'queens' in address.lower():
        boro = 'queens'
    if 'manhattan' in address.lower():
        boro = 'manhattan'
    if 'bronx' in address.lower():
        boro = 'bronx'
    if 'staten' in address.lower():
        boro = 'staten'
    if 'nj' in address.lower():
        boro = 'nj'
    if 'new york' in address.lower():
        boro = 'manhattan'

    # catch bad address'ss

    if boro == 'NONE':
        address = 'NONE'

    # set address information

    new_porfile_pic_obj['address'] = address
    new_porfile_pic_obj['boro'] = boro

    new_obj['boro'] = boro
    new_obj['address'] = address


    # get lattitude and longitude 
    try:

        lattitude = soup.find('meta', property='event:location:latitude')
        longitude = soup.find('meta', property='event:location:longitude')

        print(1)
        
    except:

        lattitude = 'NONE'
        longitude = 'NONE'

        print(2)
    
    new_obj['lattitude'] = lattitude['content']
    new_obj['longitude'] = longitude['content']
    new_porfile_pic_obj['lattitude'] = lattitude['content']
    new_porfile_pic_obj['longitude'] = longitude['content']


    # grab all full-size images & Create a new object for each

    full_size_pics = soup.find_all('img', class_='eds-max-img')

    for img in full_size_pics:

        new_obj['src'] = img['src']
        picture_list.append(copy.deepcopy(new_obj))

    # append and print
    profile_pictue_list.append(new_porfile_pic_obj)

    
    print(f'articles scraped: {i} of{total_articles}')
 

'''
write to database
'''

combined_list = picture_list + profile_pictue_list

with open(f'{DATE}_event_data.json', 'w') as file:
    json.dump(combined_list, file)





    # conn = sqlite3.connect('xda_data.db')
    # c = conn.cursor()
    # # c.execute('''CREATE TABLE xda_data (Headline text, Excerpt text, Author text, Date_posted text)''')


    # df = pd.read_csv('xda_data.csv')
    # df.to_sql('xda_data', conn, if_exists='replace', index = False)
#
    # a = c.execute('''SELECT * FROM xda_data''').fetchall()

    # print(a)
