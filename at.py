import requests
from bs4 import BeautifulSoup
from datetime import datetime,timedelta
import sys
import json
#import openpyxl
#from google.colab import files
#import io
#import pandas as pd
#import csv           

#def get_air_ticket_price(p_date, p_days):  
                 
now = datetime.now()
#delta_h = timedelta(hours=8)
#now += delta_h
#delta = timedelta(days=int(p_days))
#start_date = p_date + delta
#start_date = start_date.strftime('%Y-%m-%d')

url="https://ecapi.starlux-airlines.com/searchFlight/v2/flights/search"    
#payload = {"itineraries":[{"departure":"TPE","arrival":"NRT","departureDate":start_date}],"travelers":{"adt":1,"chd":0,"inf":0},"cabin":"eco"}
payload = {"itineraries":[{"departure":"TPE","arrival":"NRT","departureDate":"2023-04-01"},{"departure":"CTS","arrival":"TPE","departureDate":"2023-04-08"}],"travelers":{"adt":1,"chd":0,"inf":0},"cabin":"eco"}
headers = {
'content-type' : 'application/json',
'user-agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
'jx-lang': 'zh-TW'
}
response = requests.post(url,headers=headers,data=json.dumps(payload))
response.encoding ='UTF-8'

soup = BeautifulSoup(response.text, "html.parser")
rt = response.text
#print(soup.prettify())  #輸出排版後的HTML內容
result_j = json.loads(rt)
flyout_t=result_j["data"]["flights"][0]["flightDetails"][0]["departure"]["dateTime"]
flyout_a=result_j["data"]["flights"][0]["flightDetails"][0]["departure"]["airport"]
flyin_t =result_j["data"]["flights"][0]["flightDetails"][0]["arrival"]["dateTime"]
flyin_a =result_j["data"]["flights"][0]["flightDetails"][0]["arrival"]["airport"]
flyp_p  =result_j["data"]["flights"][0]["priceInfo"][0]["from"]["amount"]
flyp_c  =result_j["data"]["flights"][0]["priceInfo"][0]["from"]["currencyCode"]
#flyout_t=str(flyout_t[:10])
#flyin_t=str(flyin_t[:10])
final_result = '星宇航空 STARLUX,'+flyout_a+', → ,'+flyin_a+', 經濟艙1張,'+flyout_t+', 起飛,'+flyin_t+', 抵達'+',票價 ,'+flyp_c+','+str(flyp_p)
print(final_result)


#以下是抓油價的
now = datetime.now()           
delta = timedelta(days=int(30))
start_date = now + delta
start_date = start_date.strftime('%Y-%m-%d')

url="https://www2.moeaboe.gov.tw/oil111"
headers = {
'content-type' : 'text/html',
'user-agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
'jx-lang': 'zh-TW'
}
response = requests.post(url,headers=headers)
response.encoding ='UTF-8'

soup = BeautifulSoup(response.text, "html.parser")
#print(soup.prettify())  #輸出排版後的HTML內容

div_iwr = soup.find(class_="row row-cols-1 px-4")
#print(div_iwr)
#取西德州油價
div_fn = div_iwr.find(class_="col-5 text-right")
#print(div_fn)    
div_fn2 = div_iwr.find_all("strong" ,limit=1)      #陣列
wti_oil_price=""
for wti_p in div_fn2:
    wti_oil_price = wti_p.text
    #print(wti_oil_price)
    
    
#取更新日期
div_fp = div_iwr.find(class_="col-lg-5 text-sm-right more_info_container mt-4 mt-lg-0")   #一串
#print(div_fp)  
t_sma = div_fp.find_all("small" ,limit=1)      #陣列
wti_oil_date=""
for wti_d in t_sma:
    wti_oil_date = wti_d.text.lstrip()   #去空白
    wti_oil_date = wti_oil_date[11:21]   #擷取字串位置
#print(wti_oil_date)
re_wti_oil_date = wti_oil_date.replace('/', '-')   #替代日期斜線換-
final_result = '國際原油價格-西德州(WTI): '+re_wti_oil_date+' USD/桶$:'+wti_oil_price
print(final_result)

 
