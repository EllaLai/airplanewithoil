import requests
from bs4 import BeautifulSoup
from datetime import datetime,timedelta
import sys
import json
            

def get_air_ticket_price(p_date, p_days):                    
    #now = datetime.now()
    delta = timedelta(days=int(p_days))
    start_date = p_date + delta
    start_date = start_date.strftime('%Y-%m-%d')

    url="https://ecapi.starlux-airlines.com/searchFlight/v2/flights/search"    
    payload = {"itineraries":[{"departure":"TPE","arrival":"NRT","departureDate":start_date}],"travelers":{"adt":1,"chd":0,"inf":0},"cabin":"eco"}
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
    final_result = '\n星宇航空 STARLUX\n'+flyout_a+' → '+flyin_a+' 經濟艙單程票1張\n'+flyout_t+' 起飛\n'+flyin_t+' 抵達\n'+'票價 '+flyp_c+' '+str(flyp_p)
    print(final_result)

    #spid = '2'
    #sid = '179'
    headers = {
        "Authorization": "Bearer " + "NNOck7uv9oiT73CIxly4fYyrU96iSN14sMTCtpQuxb0",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    #params = {"message": final_str,"stickerPackageId": spid,"stickerId": sid}
    params = {"message": final_result}
    #print(params)
    r = requests.post("https://notify-api.line.me/api/notify",headers=headers, params=params)
    print(r.status_code)  #200            
    
if __name__ == '__main__':
    try:
        date, days= sys.argv[1:3]
        get_air_ticket_price(date, days)
    except Exception as e:
        now = datetime.now()
        date=now
        days='30'
        get_air_ticket_price(date, days)    