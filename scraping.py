#!/usr/bin/env python
# coding: utf-8

# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt


def scrape_all():
  executable_path = {'executable_path': ChromeDriverManager().install()}
  browser = Browser('chrome', **executable_path, headless=True)

  news_title, news_paragraph = mars_news(browser)

  #Run all scraping functions and store the data in dictionary
  data = {
    "news title": news_title,
    "news_paragraph": news_paragraph,
    "featured_image": featured_image(browser),
    "facts": mars_facts(),
    "last_modified": dt.datetime.now(),
    "hemisphere" : hemisphere(browser)
  }

  #Stop webdriver and reture data
  browser.quit()
  return data



#create a function to scrape news title and summary
def mars_news(browser):

  #Visit the Mars NASA news site
  url = 'https://redplanetscience.com'
  browser.visit(url)

  #Optional delay for loading page
  browser.is_element_present_by_css('div.list_text, wait_time=1')

  #Set up the parser
  html = browser.html
  news_soup = soup(html, 'html.parser')
  
  #Add try/except for error handling
  try:
    slide_elem = news_soup.select_one('div.list_text')

    slide_elem.find('div', class_='content_title')

    news_title = slide_elem.find('div', class_= 'content_title').get_text()
    news_p = slide_elem.find('div', class_= 'article_teaser_body').get_text()
  
  except AttributeError as e:
    print(f"an error occured {e}")
    return None, None
  return news_title, news_p


  # ### Featured Images

def featured_image(browser):

  #Visit URL 
  url = 'https://spaceimages-mars.com'
  browser.visit(url)

  #Find and clock the full image button
  full_image_elem = browser.find_by_tag('button')[1]
  full_image_elem.click()

  #Parse the resulting html with soup
  html = browser.html
  img_soup = soup(html, 'html.parser')

  #Find the relative image url
  try:
    img_url_rel = img_soup.find('img', class_ = 'fancybox-image').get('src')
  except AttributeError as e:
    print(f"an error occured {e}")
    return None, None  

  #Use the base URL to create an absolute URL
  img_url = f'https://spaceimages-mars.com/{img_url_rel}'
  
  return img_url

#Scrape a table
def mars_facts():

  try:
    df = pd.read_html('https://galaxyfacts-mars.com')[0]
  except BaseException as e:
    print(f"an error occured {e}")
    return None
  
  df.columns=['description', 'Mars', 'Earth']
  df.set_index('description', inplace=True)

  #Convert table to html
  return df.to_html(classes="table table-striped")

if __name__ == "__main__":

  #If running as csript, print scrapped data
  print(scrape_all())


def hemisphere(browser):
  url = 'https://marshemispheres.com/'

  browser.visit(url)

  # 2. Create a list to hold the images and titles.
  hemisphere_image_urls = []

  #  3. Write code to retrieve the image urls and titles for each hemisphere.
  for hemi in range(4):
    browser.links.find_by_partial_text('Hemi')[hemi].click()
    
    #Parse the html 
    html = browser.html
    hemi_soup = soup(html, 'html.parser')
    
    #Scraping
    image = hemi_soup.find('li').a.get('href')
    title = hemi_soup.find('h2', class_='title').text
    
    #Store the results in a dictionary
    hemis = {}
    hemis['image_url'] = f"https://marshemispheres.com/{image}"
    hemis['title'] = title
    hemisphere_image_urls.append(hemis)
        
    browser.back()

  return hemisphere_image_urls
    
#Shut down the brownser
# browser.quit()

