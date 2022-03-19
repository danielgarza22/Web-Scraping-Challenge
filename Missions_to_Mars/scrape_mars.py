import pandas as pd
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
from splinter import Browser
import requests
import os
import time

def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    t, p = news(browser)

    data = {
        'title': t,
        'paragraph': p,
        'image': image(browser),
        'facts': facts(),
        'hemispheres': hem(browser)
    }
    browser.quit()
    return data

def news(browser):
    news_url = 'https://redplanetscience.com/'
    browser.visit(news_url)
    time.sleep(2)
    html = browser.html
    news_soup = bs(html, 'html.parser')
    news_title = news_soup.find('div', class_='content_title').text
    news_p = news_soup.find('div', class_='article_teaser_body').text
    return news_title,news_p

def image(browser):
    space_image_url = 'https://spaceimages-mars.com/'
    browser.visit(space_image_url)
    img_html = browser.html
    image_soup = bs(img_html, 'html.parser')
    space_image = image_soup.findAll('img', class_='headerimage fade-in')[0]["src"]
    return space_image_url + space_image


def facts():
    facts_url = 'https://galaxyfacts-mars.com/'
    tables = pd.read_html(facts_url)
    mars_table_df = tables[0]
    mars_table_df.columns = mars_table_df.iloc[0]
    mars_table_df = mars_table_df.iloc[1: , :]
    return mars_table_df.to_html(index=False)


def hem(browser):
    hem_url = 'https://marshemispheres.com/'
    browser.visit(hem_url)
    hem_html = browser.html
    hem_soup = bs(hem_html, 'html.parser')
    hem_items = hem_soup.find_all('div', class_='item')
    hem_img_urls = []

    for hem_item in hem_items:
        img_link = hem_url + hem_item.find('a')['href']
        browser.visit(img_link)
        item_html = browser.html
        item_soup = bs(item_html, 'html.parser')
        img_link2 = hem_url + item_soup.find('img',class_='wide-image')['src']
        hem_name = hem_item.find('div',class_='description').find('a').text.replace('\n','')[:-9]
        item_dict = {"title":hem_name,"img_url":img_link2}
        hem_img_urls.append(item_dict)
    
    return hem_img_urls
