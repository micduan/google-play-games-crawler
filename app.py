from flask import Flask, render_template
from flask_bootstrap import Bootstrap

from models.GameCategories import Category
import time
import collections

from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

def WaitforElement(browser, timeout, xpathElement):
	try:
	    WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, xpathElement)))
	except TimeoutException:
	    print("Timed out waiting for page to load")
	    browser.quit()

app = Flask(__name__)
Bootstrap(app) # use bootstrap

action_url = "https://play.google.com/store/apps/category/GAME_ACTION?hl=en"

browser = webdriver.Chrome()
browser.get(action_url)



#game categories objects of all game titles and category
all_game_categories = collections.OrderedDict()

title_categoryElements = browser.find_elements_by_xpath('//a[@class="title-link id-track-click"]') # get all the Title buttons
title_categories = [(x.text, x.get_attribute('href')) for x in title_categoryElements]
for title in title_categories:
	browser.get(title[1])

	game_title_elements = browser.find_elements_by_xpath('//a[@class="title"]')
	gameTitles = [elem.text for elem in game_title_elements]

	all_game_categories[title[0]] = gameTitles

category_wrappers = []
for category, gamelist in all_game_categories.items():
	game_titles_per_category = Category(category, gamelist)
	category_wrappers.append(game_titles_per_category)


@app.route('/')
def index():
	return render_template('home.html', all_game_categories = category_wrappers)

if __name__ == '__main__':
	app.run()