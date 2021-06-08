#!/usr/local/bin/python3.7

### FB video download

import io
import os
import sys
import re
import time
import json
import requests
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException

if len(sys.argv) == 1:
	print("Usage: ./fbvidwo_download.py URL_TO_FB_VIDEO ")
	exit()

fb_url = sys.argv[1]
fb_id = re.search("[0-9]+",fb_url).group(0)
print("Input FB Video link: " + fb_url)

chromeOptions = webdriver.ChromeOptions() 
chromeOptions.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2}) 
chromeOptions.add_argument("--no-sandbox") 
chromeOptions.add_argument("--disable-setuid-sandbox") 

chromeOptions.add_argument("--remote-debugging-port=9222")  # this

chromeOptions.add_argument("--disable-dev-shm-using") 
chromeOptions.add_argument("--disable-extensions") 
chromeOptions.add_argument("--disable-gpu") 
chromeOptions.add_argument("--headless") 
chromeOptions.add_argument("start-maximized") 
#chromeOptions.add_argument("disable-infobars")
#chromeOptions.add_argument(r"user-data-dir=.\cookies\\test") 

caps = DesiredCapabilities.CHROME
caps['goog:loggingPrefs'] = {'performance': 'ALL'}
driver = webdriver.Chrome(options=chromeOptions, desired_capabilities=caps, service_args=["--verbose"])
#driver = webdriver.Chrome(options=chromeOptions, desired_capabilities=caps, service_args=["--verbose", "--log-path=./chrome.log"])
driver.get(fb_url)
time.sleep(5)
try:
	e1 = driver.find_element_by_xpath("//div[@class='_8frr']")
	e1.click()
except NoSuchElementException:
	driver.close()
	exit()

time.sleep(10)

performance_data = driver.execute_script("return window.performance.getEntries();")

time.sleep(5)

driver.close()

min_v = 9999999
max_v = -1
for x in range(len(performance_data)):
	y = performance_data[x]["name"]
	if y.find("bytestart") != -1:
		z = performance_data[x]["decodedBodySize"]
		if z > max_v:
			max_v = z
			max_y = y
		elif z < min_v:
			min_v = z
			min_y = y


min_y = re.sub('&bytestart.*$','',min_y)
max_y = re.sub('&bytestart.*$','',max_y)

fb_audio_fn = fb_id + "_audio.mp4"
fb_video_fn = fb_id + "_video.mp4"
fb_output = fb_id + ".mp4"

print("Downloading audio file....")
r = requests.get(min_y, allow_redirects=True)
open(fb_audio_fn, 'wb').write(r.content)

print("Downloading video file....")
r = requests.get(max_y, allow_redirects=True)
open(fb_video_fn, 'wb').write(r.content)

#print("Output mp4 file: " + fb_id + ".mp4")
#command = "/usr/bin/ffmpeg -loglevel error -i " + fb_video_fn + " -i " + fb_audio_fn + " -c copy " + fb_output
#output_txt = os.system("/usr/bin/ffmpeg -loglevel panic -i " + fb_video_fn + " -i " + fb_audio_fn + " -c copy " + fb_id + ".mp4")
#subprocess.call(command,shell=True)
#subprocess.call(['ffmpeg', '-loglevel', 'error', '-i', fb_video_fn, '-i', fb_audio_fn, '-c', 'copy', fb_output])
#if os.path.exists(fb_id + ".mp4"):
#	os.remove(fb_audio_fn)
#	os.remove(fb_video_fn)
#else:
#	print("File output error")

