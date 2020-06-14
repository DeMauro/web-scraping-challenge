#import dependencies

from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import time

def init_browser():
    chrome = "/Users/frama/data-class/web-scraping-challenge/Missions_to_Mars/chromedriver.exe"
    executable_path = {'executable_path': chrome}
    return Browser("chrome", **executable_path, headless=True)

def scrape():
    browser = init_browser()

    # dictonary for data
    mars_stuff = {}

    # Scrape the NASA Mars News Site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(5)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    list_text = soup.find('div', class_='list_text')
    news_title = list_text.find('a').text
    news_p = soup.find('div', class_='article_teaser_body').text
    mars_stuff["news_title"] = news_title
    mars_stuff["news_p"] = news_p

    # JPL Mars Space Images - Featured Image
    pic_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(pic_url)
    pic_html = browser.html
    soup = BeautifulSoup(pic_html, 'html.parser')

    image = soup.find("a", class_="button fancybox")["data-link"]
    step_two = "https://jpl.nasa.gov"+image
    browser.visit(step_two)
    step_two_html = browser.html
    soup = BeautifulSoup(step_two_html, 'html.parser')

    lede = soup.find("figure", class_="lede")
    pic_title = lede.find('a')['href']
    featured_image_url = "https://jpl.nasa.gov"+pic_title
    mars_stuff["featured_image_url"] = featured_image_url

    # Mars Weather
    twit_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twit_url)
    while True:
        if not browser.is_element_not_present_by_tag('article'):
            break
    twit_html = browser.html
    soup = BeautifulSoup(twit_html, 'html.parser')
    tweets = soup.find('article')
    for tweet in tweets:
        spans = tweet.find_all("span")
        mars_weather = spans[4].get_text()
    mars_stuff["mars_weather"] = mars_weather

    # Mars Facts
    fact_url = 'https://space-facts.com/mars/'
    browser.visit(fact_url)
    fact_html = browser.html
    soup = BeautifulSoup(fact_html, 'html.parser')
    facts=pd.read_html(fact_url)
    mars_data=pd.DataFrame(facts[0])
    mars_data.columns=['description','value']
    mars_table=mars_data.set_index("description")
    marsdata = mars_table.to_html(classes='marsdata')
    marsdata=marsdata.replace('\n', '')
    mars_stuff["mars_facts"] = marsdata

    # Mars Hemispheres
    hemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemi_url)
    hemi_html = browser.html
    soup = BeautifulSoup(hemi_html, 'html.parser')
    hemisphere_image_urls=[]
    for thumb in range (4):    
        images = browser.find_by_tag('h3')
        images[thumb].click()
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
    
        full_guy = soup.find("li")
        img_url = full_guy.find('a')['href']
        img_title = soup.find("h2",class_="title").text
        hemisphere={
            "title":img_title,
            "img_url":img_url
        }
        hemisphere_image_urls.append(hemisphere)
        browser.back()
    mars_stuff['hemisphere_image_urls'] = hemisphere_image_urls
    
    browser.quit()
    print(mars_stuff)
    return mars_stuff