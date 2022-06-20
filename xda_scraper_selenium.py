
from selenium.webdriver import Chrome
import pandas as pd

webdriver = "/Users/rh/Desktop/Py/it/sel/chromedriver"

driver = Chrome(webdriver)


pages = 3

URL = "https://www.xda-developers.com/"

total = []
for page in range(1,pages):

    driver.get(URL)
    
    sections = driver.find_elements_by_class_name("layout_post_2")

    for section in sections:

        # print(section.text)
        articles = section.find_elements_by_class_name('item_content')
        
        for article in articles:


            headline = str(article.find_element_by_tag_name('h4').text).replace(',', '')

            excerpt = str(article.find_element_by_class_name('the-excerpt').text).replace(',', '')

            author = article.find_element_by_class_name('meta_author').text

            date_posted = article.find_element_by_class_name('meta_date').text


            new = ((headline,excerpt,author,date_posted))
            total.append(new)

        # print(driver.find_element_by_class_name('next').text)
        URL = f'https://www.xda-developers.com/page/{page+1}/'

driver.close()
df = pd.DataFrame(total,columns=['Headline','Excerpt','Author','Date_Posted'])
df.to_csv('XDA_selenium_scrape.csv')