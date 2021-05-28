# -*- coding: utf-8 -*-
#
#								ﻢﻴﺣﺮﻟا ﻥﺎﻤﺣﺮﻟا ﻪﻠﻟا ﻢﺳﺎﺑ
#						ﺮﻳﺪﻗ ءﻲﺷ ﻞﻛ ﻰﻠﻋ ﻮﻫ ﻭ ﻚﻠﻤﻟا ﻪﻟ ﻞﻛﻮﺘﻧ ﻪﻴﻠﻋ
#
####################################################################################
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.command import Command
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time
import os
import requests
import random
import datetime as dt
import codecs

from func import WebShare_Proxies
####################################################################################
tmin=6
tmax=6
t1=6
t2=12
####################################################################################
#GET LIST OF PROXIES
df_proxies=WebShare_Proxies()
args=df_proxies.values[random.choice(df_proxies.index)].tolist()

proxy_ip,proxy_port,username,password=args

proxy=redirect_traffic(args)
####################################################################################
df=pd.read_csv("amazon_credentials.txt","r",delimiter=',',header=None)
login=df.values[0][0]
passw=df.values[0][1]
####################################################################################
print('Initializing Profile...\n')
print('-----------------------------------------------------------------')
#SELENIUM ENTRIES
cap = DesiredCapabilities().FIREFOX
cap["marionette"] = True
cap['acceptInsecureCerts'] = True
binary = FirefoxBinary('/usr/bin/firefox')
##
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
#options.add_argument('--load-images=no')
options.add_argument("window-size=1400,600")
options.add_argument("user-data-dir=/tmp/tarun")
#options.add_argument('--ignore-certificate-errors')
#options.add_argument('--proxy-server=%s' % proxy)
##
profile = webdriver.FirefoxProfile()
#profile.set_preference("general.useragent.override", "[user-agent string]")
profile.set_preference("general.useragent.override", 
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:63.0) Gecko/20100101 Firefox/63.0")
####################################################################################
#GOT TO AMAZON PAGE
#url='https://www.amazon.com/'

#GO TO AMAZON LOGIN PAGE
url='https://www.amazon.com/ap/signin?_encoding=UTF8&openid.assoc_handle=usflex&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2Fgp%2Fyourstore%2Fhome%3Fie%3DUTF8%26action%3Dsign-out%26path%3D%252Fgp%252Fyourstore%252Fhome%26ref_%3Dnav_AccountFlyout_signout%26signIn%3D1%26useRedirectOnSuccess%3D1'
#url='https://fra.privateinternetaccess.com/pages/whats-my-ip/'

driver = webdriver.Firefox(profile,options = options,capabilities=cap,firefox_binary=binary)
driver.set_page_load_timeout(np.random.randint(5,10))
driver.get(url)

#NO CLICK ON LANGUAGE
#not_now_button=driver.find_element_by_xpath("//button[normalize-space()='No, thanks']")

#CLICK ON LOGIN
#login_url=driver.find_element_by_xpath("//div[@id='nav-flyout-ya-signin']")
#login_url.click()

# USERNAME
username_input = driver.find_element_by_css_selector("input[name='email']")
username_input.send_keys(login)
login_button=driver.find_element_by_id('continue')
login_button.click()
time.sleep(np.random.randint(5,10))
# PASSWORD
pass_input = driver.find_element_by_css_selector("input[name='password']")
pass_input.send_keys(passw)
#CHECK KEEP ME Signed In

pass_button=driver.find_element_by_xpath("//input[@id='signInSubmit']")
pass_button.click()

#URL BOOK
search_book='winning against all odds kevin parker'

#SEARCH BOX
search_box=driver.find_element_by_id('twotabsearchtextbox')
search_box.send_keys(search_book)
search_box.send_keys(Keys.ENTER)
time.sleep(np.random.randint(8,15))

#SEARCH PAGE
element=driver.find_element_by_xpath("//img[@class='s-image']")
driver.execute_script('var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;', element)

# CLICK ON BOOK AND VISIT THE PAGE
action = webdriver.ActionChains(driver)
action.move_to_element(element).click().perform()

# ADD TO CART BOOK
add_to_cart=driver.find_element_by_id('add-to-cart-button')
add_to_cart.click()

f = codecs.open("page_source.txt", "w", "utf−8")
h = driver.page_source
f.write(h)

#
#
#
#
#