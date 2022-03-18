#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import Dependencies
import pandas as pd
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
from splinter import Browser
import requests
import os


# In[2]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ## NASA Mars News

# In[3]:


# Mars News Website
news_url = 'https://redplanetscience.com/'
browser.visit(news_url)


# In[4]:


# Convert the browser html to a soup object
html = browser.html
news_soup = bs(html, 'html.parser')


# In[5]:


print(news_soup.prettify())


# In[6]:


# Find and print the Mars website news title
news_title = news_soup.find('div', class_='content_title').text
news_title


# In[7]:


# Find and print the Mars website news paragraph
news_p = news_soup.find('div', class_='article_teaser_body').text
news_p


# ## JPL Mars Space Image

# In[8]:


# Mars Space Images Website
space_image_url = 'https://spaceimages-mars.com/'
browser.visit(space_image_url)


# In[9]:


# Convert the browser html to a soup object
img_html = browser.html
image_soup = bs(img_html, 'html.parser')


# In[10]:


# Get space image
space_image = image_soup.findAll('img', class_='headerimage fade-in')[0]["src"]
space_image = space_image_url+space_image
print(space_image)


# ## Mars Facts

# In[11]:


# Mars Facts Website
facts_url = 'https://galaxyfacts-mars.com/'
tables = pd.read_html(facts_url)


# In[12]:


mars_table_df = tables[0]
mars_table_df.columns = mars_table_df.iloc[0]
mars_table_df = mars_table_df.iloc[1: , :]
mars_table_df


# In[13]:


mars_table_html = mars_table_df.to_html(index=False).replace('\n', '')
mars_table_html


# ## Mars Hemispheres

# In[19]:


# Mars Hemispheres
hem_url = 'https://marshemispheres.com/'
browser.visit(hem_url)


# In[20]:


hem_html = browser.html
hem_soup = bs(hem_html, 'html.parser')


# In[21]:


hem_items = hem_soup.find_all('div', class_='item')


# In[28]:


hem_img_urls = []


# In[29]:


for hem_item in hem_items:
    
    img_link = hem_url + hem_item.find('a')['href']
    
    browser.visit(img_link)
    
    item_html = browser.html
    
    item_soup = bs(item_html, 'html.parser')
    
    img_link2 = hem_url + item_soup.find('img',class_='wide-image')['src']
    
    hem_name = hem_item.find('div',class_='description').find('a').text.replace('\n','')[:-9]
    
    item_dict = {"title":hem_name,
         "img_url":img_link2}
    
    hem_img_urls.append(item_dict)


# In[30]:


hem_img_urls


# In[31]:


browser.quit()


# In[ ]:

mars_data={
    "recentTitle": news_title,
    "recentParagraph":news_p,
    "imageURL":space_image,
    "table":mars_table_html,
    "hemispheres":hem_img_urls
}

