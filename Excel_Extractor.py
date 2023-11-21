import pandas as pd
from selenium.webdriver.common.by import By
from selenium import webdriver
import time

main_driver = webdriver.Chrome()
url="https://monasebat.anhar.ir/"
main_driver.get(url)

# Lists
a_td_list = []
url_list = []
description_list = []
all_data = []

# h1_element_list = []
# event_list = []
# event_date_list = []
# form_list = []

month=0

   


# td
td_element = main_driver.find_elements(By.TAG_NAME, "td")
for td in td_element:
    try:
        a_element = td.find_elements(By.TAG_NAME, "a")
        href_element = a_element[0].get_attribute("href")
        url_list.append(href_element)
    except:
        print(".")

print("urls: ", len(url_list))


# counter = 0
dayCounter = 0
for url in url_list:
    
    main_driver.get(url)
    dayCounter += 1
    print('day',dayCounter)

    
    # Write Title Of DayPage
    h1_element = main_driver.find_element(By.TAG_NAME, "h1")
    # event_list.append(h1_element.text)

    # Find event links from every day
    article1 = main_driver.find_element(By.CLASS_NAME, "article")

    article1_links = [
        element
        for element in article1.find_elements(By.TAG_NAME, "a")
        if element.text != None and element.text != ""
    ]

    print("Len Link1 " + str(len(article1_links)))
    events_driver = webdriver.Chrome()
    event_date = ''
    index = 0
    for link in article1_links:

        # mylink = link
        mylink_href = link.get_attribute("href")
        index = index + 1
        print('day: ',dayCounter , "event",index)
        print("Next Event")
        events_driver.get(mylink_href)

        

        # Write Titles Of EventPage
        title = events_driver.find_element(By.TAG_NAME, "h1")
        # event_date = events_driver.find_element(By.TAG_NAME,'a')
        # title = event_date.__getattribute__("title")
        # title_class = main_driver.find_element(By.CLASS_NAME, "event")
        # title_text = title_class.get_attribute('title')

        # event_date_list.append(title.text)

        # Find Descirption content of every event
        context = events_driver.find_element(By.CLASS_NAME, "article")

        article2_spans = [
            span_element
            for span_element in context.find_elements(By.TAG_NAME, "span")
            if span_element.text != None and span_element.text != ""
        ]

        description = []
        article2_span_contents = []

        # Distinct content
        for span in article2_spans:

            if span.text in description:
                continue
            else:
                article2_span_contents.append(span.text)
                description.append(span.text)

        for element in description:
            description_list.append(element + "\n")

        data={
        'event':h1_element.text,
        'date':title.text,
        'details':description,
        }
        
        all_data.append(data)
        # counter += 1

        # if counter == 3:
        file=pd.DataFrame(all_data)
        file.to_excel('Extracted.xlsx',index=False, engine='openpyxl')      


    events_driver.close()       

main_driver.quit()