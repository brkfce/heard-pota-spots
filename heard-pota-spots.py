# small app to notify you when a spot on the pota.app website can actually be heard, by comparing to spots from a local rbn node.

import configparser
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re
import requests

def get_settings(settings_path):

	config = configparser.ConfigParser()
	try:
		config.read(settings_path)
	except:
		print('Failed to read settings.ini file')
		exit()

	settings = config['config']
	
	return settings


def get_rbn_spots(rbn_node, driver_options):

	rbn_url = 'https://reversebeacon.net/main.php?max_age=10,minutes&rows=100&modes=cw&spot_types=1,2,3,4,5&spotter_call=' + rbn_node + '&hide=distance_km'

	# get dynamic content from RBN
	driver = webdriver.Firefox(options=driver_options)
	try:
		driver.get(rbn_url)
	except:
		print('Failed to get RBN content')
		exit()
	# wait for elements to load
	time.sleep(10)
	rbn_content = driver.page_source
	driver.quit()

	# list all calls heard by selected node
	rbn_regex = 'dx ([A-Z]+[0-9]+[A-Z]+)'
	heard_calls = re.findall(rbn_regex, rbn_content)
	return heard_calls


def get_pota_spots(driver_options):

	pota_url = 'https://pota.app'
	
	# get dynamic content from pota.app
	driver = webdriver.Firefox(options=driver_options)
	try:
		driver.get(pota_url)
	except:
		print('Failed to get pota.app content')
		exit()
	# wait for elements to load
	time.sleep(10)
	pota_content = driver.page_source
	driver.quit()
	
	# test: list all calls found
	pota_regex = ' ([A-Z]+[0-9]+[A-Z]+)'
	found_calls = re.findall(pota_regex, pota_content)

	return found_calls


def main() -> None:
	settings_path = 'settings.ini'
	settings = get_settings(settings_path)
	
	if settings['browser'] == 'firefox':
		driver_options = webdriver.FirefoxOptions()
	elif settings['browser'] == 'chrome':
		driver_options = webdriver.ChromeOptions()
	else: 
		print('Invalid browser selected in settings.ini, please amend')
		exit()

	driver_options.add_argument('--headless=new')

	rbn_node = settings['local_rbn']
	rbn_spots = get_rbn_spots(rbn_node, driver_options)

	# I was going to try and filter the POTA website content by mode so we only get CW spots, but we'll only get CW spots from RBN... so no non-CW spot will come through when we compare lists!
	pota_spots = get_pota_spots(driver_options)
	
	# find spots that appear on both RBN and POTA
	matches = set(pota_spots).intersection(rbn_spots)
	
	
	# send matches to discord channel
	webhook = settings['webhook']
	
	for spot in matches:
		
		print(rbn_node + ' just heard ' + spot + '!')
		try:
			message = '' + rbn_node + ' just heard ' + spot + '!'
			message_package = {"content": message}
			send_discord = requests.post(webhook, json=message_package)
		except:
			print('Failed to send discord message; is the webhook url correct?')
			exit()

	if len(matches) == 0:
		print('No matches found this round!')

while(True):
	main()
	time.sleep(60)
