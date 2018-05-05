from flask import Flask, render_template, jsonify, redirect
import pymongo
from bs4 import BeautifulSoup
from selenium import webdriver
from splinter import Browser
import time
import pandas as pd
import json
import scrape_mars


app = Flask(__name__)

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.marsdata
collection = db.marsdata

@app.route('/scrape')
def scrape():
	articleTitle,articleP =  scrape_mars.get_new_mars_article()
	featureImageUrl = scrape_mars.get_featured_image_url()
	marsFactsTable =  scrape_mars.get_mars_facts()
	marsWeather =  scrape_mars.get_mars_weather()
	hemisphereImagesDict = scrape_mars.get_hemisphere_images()
	updateJSON = {
			'articleTitle':articleTitle,
			'articleText':articleP,
			'featuredImg':featureImageUrl,
			'marsWeather':marsWeather,
			'marsFactsTable':marsFactsTable,
			'hemImages': hemisphereImagesDict
			}
	db.collection.update(
		{},
		updateJSON,
		upsert=True
	)
	return redirect("http://localhost:5000/", code=302)

@app.route('/')
def index():
	# @TODO: write a statement that finds all the items in the db and sets it to a variable
	marsDataJSON = list(db.collection.find())
	# @TODO: render an index.html template and pass it the data you retrieved from the database
	return render_template("index.html" , marsJSON=marsDataJSON[0])

if __name__ == "__main__":
    app.run(debug=True)
