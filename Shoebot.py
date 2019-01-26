'''
Created on Dec 3, 2018

@author: Lester H
'''
import requests
import json
from _weakref import proxy
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from lib2to3.tests.support import driver


#base url = https://www.adidas.com/us/yung-96-shoes/EE3682.html?forceSelSize=EE3682_600
def urlGen(model, size):
    Basesize = 580
    #Basesize is the smallest shoe size available 6.5
    Shoesize  = int(size) - 6.5
    Shoesize = Shoesize * 20
    RawSize = Shoesize + Basesize
    ShoesizeCode = int(RawSize)
    URL = 'https://www.adidas.com/us/' + str(model) + '.html?forceSelSize=' + str(model) + '_' + str(ShoesizeCode)
    return URL


def SizeAvailable(model):
    api_url = "https://www.adidas.com/api/products/%s/availability?sitePath=us" % (str(model))
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}                                                                                   
    
    response = requests.get(api_url, headers = headers)
    source = response.text
    data = json.loads(source)
    
    for numsize in data['variation_list']:
        shoe_size = numsize['size']
        shoe_available = numsize['availability_status']
        if shoe_available == 'IN_STOCK':
            print(shoe_size)
        else:
            print(shoe_size,'|', 'Out of stock')
            
    return headers
            
def Printthis():
    print('You just did something')
    
def addtocart(model, size = None):
    cart_url = 'https://www.adidas.com/api/cart_items?sitePath=us'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}  
    response = requests.get(cart_url, headers = headers)
    source = response.text
    json.loads(source)
    
    driver = webdriver.Chrome()
    driver.get(urlGen(model,size))
    driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/div[2]/div/div[3]/div[3]/div[3]/div/div/form/div[3]/button')
    
    
    while True:
        try:
            url = 'https://www.adidas.com/us/{}.html?'.format(model)
            Sizes = SizeAvailable(url)
            if size != None:
                if str(size) in Sizes:
                    Printthis()
            else:
                for i in Sizes:
                    Printthis()
        except:
            pass
        
def Main(model, size, proxy):
    URL = urlGen(model, size)
    SizeAvailable(model)
    