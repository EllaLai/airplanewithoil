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
