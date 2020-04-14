from selenium import webdriver
import pandas as pd
import unicodedata
from selenium.common.exceptions import NoSuchElementException
import time
import datetime
import numpy as np
import re


login = '79251156234'
password = 'Aristotel31'
link_raw = 'https://m.facebook.com/groups/470640109647012/?ref=group_browse'
s = "13/04/2020"
start_date = int(time.mktime(datetime.datetime.strptime(s, "%d/%m/%Y").timetuple()))

# Преобразовывает ссылку к виду с лентой в хронологическом порядке
def link_creator(link):
    link_splitted = link.split('/')
    id = link_splitted[4]
    url = 'https://www.facebook.com/groups/' + id +'/?sorting_setting=CHRONOLOGICAL'
    return url,id

# функция скролла страницы
def scroll():
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# проверяет не достигли ли итерации нужной даты
def date_checking(dates_code):
    for i in range(len(dates_code)):
        dates.append(dates_code[i].get_attribute('data-utime'))

        if (float(dates[i]) < start_date) and i > 0:
            stop == 1
            quant_of_posts = i
            return quant_of_posts


driver = webdriver.Chrome('/Users/alex_nau/Desktop/chrm/chromedriver')
driver.get('https://m.facebook.com/login/?next=https%3A%2F%2Fm.facebook.com%2Fgroups_browse%2Fyour_groups%2F')
driver.implicitly_wait(10)
button1 = driver.find_element_by_id('m_login_email')
button1.click()
button1.send_keys(login)

button1 = driver.find_element_by_id('m_login_password')
button1.click()
button1.send_keys(password)
button3 = driver.find_element_by_id('u_0_4')
button3.click()
driver.implicitly_wait(10)

# проверяем в каких группах есть обновления
groups = driver.find_elements_by_class_name('_7hkg')
ids = []
links_raw = []
for i in range(len(groups)):
    ids.append(str(groups[i].get_attribute('href')))

    t = groups[i].text.split('\n')
    if len(t) == 3:
        if int(''.join(filter(str.isdigit, t[2]))) > 0:
            links_raw.append(str(ids[i]))
            print(ids[i])
        i = i + 2
    else:
        i = i + 2
        continue
text_file = open("/Users/alex_nau/PycharmProjects/parcer/facebook.html", "w")
output_html = '<html>\n<body>\n\t<script async defer src="https://connect.facebook.net/en_US/sdk.js#xfbml=1&version=v3.2"></script>\n'
# переходим по полученным ссылкам и вытаскиваем посты и даты
for link_raw in links_raw:
    link,id = link_creator(link_raw)

    driver = webdriver.Chrome('/Users/alex_nau/Desktop/chrm/chromedriver')
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    chrome_options.add_experimental_option("prefs",prefs)
    driver = webdriver.Chrome(chrome_options=chrome_options)

    driver.get(link)
    driver.implicitly_wait(10)

    button1 = driver.find_element_by_id('email')
    button1.click()
    button1.send_keys(login)

    button1 = driver.find_element_by_id('pass')
    button1.click()
    button1.send_keys(password)
    button3 = driver.find_element_by_id('u_0_2')
    button3.click()
    driver.implicitly_wait(10)


    stop = 0
    while(stop == 0):
        # в этом классе у нас находится ссылка на пост, в дочернем abbr - его дата
        posts = driver.find_elements_by_class_name('_5pcq')

        dates = []
        dates_code = []
        links = []
        posts_sorted = []

        for i in posts:
            if (i.get_attribute('href')).find('groups') != -1:
                posts_sorted.append(i)
                links.append(i.get_attribute('href'))


        for l in posts_sorted:
            try:
                dates_code.append(l.find_element_by_xpath('.//abbr'))
                driver.implicitly_wait(3)
            except NoSuchElementException:

                continue

        for i in range(len(dates_code)):
            dates.append(dates_code[i].get_attribute('data-utime'))


        if date_checking(dates_code):
            stop = 1
            quant_of_posts = date_checking(dates_code)

        scroll()



    dates_final = []
    links_final = []
    for i in range(quant_of_posts):
        dates_final.append(datetime.datetime.fromtimestamp(int(dates[i])).strftime('%Y-%m-%d %H:%M:%S'))
        links_final.append(links[i])

    # output_html = '<html>\n<body>\n\t<script async defer src="https://connect.facebook.net/en_US/sdk.js#xfbml=1&version=v3.2"></script>\n'
    for i in range(len(links)):
        link = str(links[i])
        output_html += '\t<div class="fb-post" data-href="%s" data-width="500"></div>\n' % links[i]

    # output_html += '</body>\n</html>'
    # text_file = open("/Users/alex_nau/PycharmProjects/parcer/facebook.html", "w")

    text_file.write(output_html)
    # text_file.close()

output_html += '</body>\n</html>'
text_file.close()