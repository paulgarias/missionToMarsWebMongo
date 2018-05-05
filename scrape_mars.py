from bs4 import BeautifulSoup
from selenium import webdriver
from splinter import Browser
import time
import pandas as pd
import json


def get_new_mars_article():
	url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
	browser = webdriver.PhantomJS(executable_path='/Users/pgarias/Downloads/phantomjs-2.1.1-macosx/bin/phantomJS')
	browser.get(url)
	html = browser.page_source
	soup = BeautifulSoup(html, 'html.parser')
	
	listArticleSlides = soup.find_all("div",class_="list_text")
	article_titles = [items.find_all("div",class_="content_title")[0].text for items in listArticleSlides]
	article_p = [items.find_all("div",class_="article_teaser_body")[0].text for items in listArticleSlides]
	return article_titles[0],article_p[0]


def get_featured_image_url():
	browser = Browser()
	browser.visit('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars')
	browser.find_by_css(".articles").first.\
	    find_by_tag("a").first.\
	    find_by_css(".img").first.\
	    find_by_tag("img").first.click()
	time.sleep(3)
	browser.find_link_by_partial_text("more info").first.click()
	browser.find_by_css(".main_image").first.click()
	imgElement = browser.find_by_tag("img")
	featured_image_url = imgElement.first['src']
	browser.quit()
	return featured_image_url


def get_mars_weather():
	browser = Browser()
	browser.visit('https://twitter.com/marswxreport?lang=en')
	mars_weather = browser.find_by_id("stream-items-id")[0].find_by_tag("li").first.find_by_css('.js-tweet-text-container').first.text
	browser.quit()
	return mars_weather

def get_mars_facts():
	dfMarsTable, = pd.read_html("https://space-facts.com/mars/")
	dfMarsTable = dfMarsTable.rename(columns={0:"Mars Facts",1:"Data"})
	marsFactsTable = dfMarsTable.to_html(index=False)
	return marsFactsTable

def get_hemisphere_images():
	browser = Browser()
	browser.visit('https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars')
	
	urlsHemispheres = [item.find_by_tag("a")[0]['href'] for item in browser.find_by_css(".description")]
	hemisphereTitles = [item.find_by_tag("h3")[0].text[:-9] for item in browser.find_by_css(".description")]
	
	
	hemisphere_image_urls=[]

	for urlSelected,titleSelected in zip(urlsHemispheres,hemisphereTitles):
		browser.visit(urlSelected)
		time.sleep(2)
		browser.find_by_css(".downloads")[0].find_by_text("Sample")
		hemisphere_image_urls.append({'title':titleSelected,'img_url':browser.find_by_css(".downloads")[0].find_by_text("Sample")[0]['href']})
	
	browser.quit()
	return hemisphere_image_urls
