
# coding: utf-8

# In[1]:


import re
import urllib2
import urllib
from bs4 import BeautifulSoup
import requests
import random
import time
import random
import pandas as pd
import numpy as np
import bs4


# In[2]:


def select_random_proxy(proxy_sf):
    row_num = random.randint(0, len(proxy_sf) - 1)
    proxy_ip = "http://{}:{}@{}:{}".format(proxy_sf.iloc[row_num]['user'],
                                               proxy_sf.iloc[row_num]['pass'],
                                               proxy_sf.iloc[row_num]['ip'],
                                               proxy_sf.iloc[row_num]['port'])
    proxy = {"http": proxy_ip, "https":proxy_ip}
    return proxy
proxies = pd.read_csv('proxies_15Apr.csv',sep=':')


# In[3]:


def select_random_UserAgent(UseragentList):
    row_num = random.randint(0, len(UseragentList) - 1)
    return UseragentList['User-agent'].iloc[row_num]


# In[4]:


List=pd.read_csv('useragent - Sheet1 (1).csv')


# In[5]:


headers = {"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
           "accept-encoding": "gzip, deflate, br",
           "accept-language": "en-GB,en-US;q=0.9,en;q=0.8,pl;q=0.7",
           "cache-control": "max-age=0",
           "referer": "www.amazon.com",
           "upgrade-insecure-requests":"1",
           "user-agent": select_random_UserAgent(List)}


# In[6]:


def get_product_list(page,base_url,Category):

    FinalList=[]
    for i in range(1,page):
        aa=0
        while aa<7:
            try:
                page_url = base_url.format(i)

                time.sleep(random.randint(2,8))
                headers['User-agent']=select_random_UserAgent(List)
                #headers['referer']= base_url.format(i)
                print page_url
                res = requests.get(page_url,headers=headers,proxies=select_random_proxy(proxies))
                print str(res.status_code)
                if '403' in str(res.status_code) or '503' in str(res.status_code):
                    time.sleep(random.randint(2,20))
                    aa=aa+1
                else:
                    soup = bs4.BeautifulSoup(res.text,'html5lib')
                    Parent = soup.find_all(True,{"class":"s-result-item"})
                    #print(Parent)
                    for product in Parent:

                        try:
                            PName=product.find("a",{"class": "a-text-normal"}).text.strip()
                            print PName
                        except:
                            PName=None
                        try:   
                            PUrl=product.find("a",{"class": "a-link-normal a-text-normal"})
                            Url=PUrl['href']
                            #print Url
                        except:
                            Url=None
                        try:
                            Pprice=product.find("span",{"class":"a-offscreen"}).text.strip()
                            #print Pprice
                        except:
                            Pprice=None
                        try:
                            Papa=product.find("span",{"class":"a-declarative"})
                            #print Papa
                            #Srating=papa.find("span",{"class":"a-icon-alt"}).text
                            star_rating=Papa.text.strip()
                            #print star_rating
                        except:
                            star_rating=None
                        try:
                            reviews=product.find_all('a')
                            for count_a in reviews:
                                reviews_url=count_a['href']
                                #print reviews_url, 'customerReviews'.lower() in reviews_url.lower()
                                if 'customerReviews'.lower() in reviews_url.lower():
                                    review = count_a.text.replace(',','').replace('\n','')
                                    break
                                else:
                                    review = None
                        except:
                            review=None
                        #print review
                        try:
                            Pimage=product.find("img",{"class":"s-access-image cfMarker"})
                            image=Pimage['src']
                            #print image
                        except:
                            image=None

                        source = {'product_name':PName,
                                  'product_url':"https://www.amazon.com"+Url,
                                  'price':Pprice,
                                  'image_url':image,
                                  'review_count':review,
                                  'star_rating':star_rating}

                        FinalList.append(source)
                    aa=7
                    
            except Exception as ex:
                print('Error', ex)
                aa=aa+1
        temp=pd.DataFrame(FinalList)
        temp.to_csv(Category+'.csv',encoding='utf-8')
    print('Done')
    return FinalList


# In[7]:


CategoryList=pd.read_csv('Amazon.com_smartphones.csv')

for cat in range(len(CategoryList)):
    
    Category=CategoryList['Category'].iloc[cat]
    CatList=CategoryList['Category_Link'].iloc[cat]
    
    base_url=CatList[:-1]+'{}'
    print base_url.format(1)
    
    ##### Enter Code of Finding Page No.
    headers['User-agent']=select_random_UserAgent(List)
    r=requests.get(base_url.format(1),headers=headers,proxies=select_random_proxy(proxies))
    soup = bs4.BeautifulSoup(r.text,'html5lib')
    inforbar=soup.find("span",{"data-component-type":"s-result-info-bar"})
    #print inforbar
    page=inforbar.find("div",{"class":"a-section a-spacing-small a-spacing-top-small"})
    count_nums = re.findall('\d+', page.text.replace(',',''))
    if(len(count_nums)==0):
        pages=100
    else:
        total_count = int(count_nums[-1])
        print total_count
        pages = total_count / 24 + bool(total_count%24)
        
    print(pages)
    CatData=get_product_list(pages,base_url,Category)
    CatData=pd.DataFrame(CatData)
    CatData.to_csv(Category+'_ProductList.csv',encoding='utf-8')
    print("Done for {}".format(Category))
    
print('Done')

