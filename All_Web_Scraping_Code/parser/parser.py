import requests
from bs4 import BeautifulSoup
import socket
import urllib2
import random
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException
import socket
import pdb

def get_browser(user_agents_list):
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    hdr = {'User-Agent': random.choice(user_agents_list),
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'}
    dcap["phantomjs.page.customHeaders"] = hdr
    browser = webdriver.PhantomJS(desired_capabilities=dcap)
    return browser

def get_url_content(data, browser, element_xpath=None):

    #socket.setdefaulttimeout(random.randint(5,7))
    try:
        browser.get(data['url'])
    except socket.timeout as ex :
        print str(type(ex).__name__)
        return None

    print data['url']

    if element_xpath:
        try:
            ele = WebDriverWait(browser, 10).until(lambda browser: browser.find_element_by_xpath(element_xpath))
        except TimeoutException, err :
            print str(type(err).__name__)
    
    content = browser.page_source
    return BeautifulSoup(content, 'html.parser')

    
