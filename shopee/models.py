from django.db import models
from bs4 import BeautifulSoup as bs
import requests
import json
  
from abc import ABC, abstractmethod

# Create your models here.
class Website(ABC):
    def __init__(self, product_name):
        self.product_name = product_name  
    
    
    @abstractmethod
    def scrape(self): 
        pass

class Shopee(Website):
  
    def scrape(self):
        result = []

        if self.product_name:
            headers = {
                'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
                'x-request-id':'api.sg3.1amFD41XWgfJEYe9mueKm2',
                'referer':'https://shopee.tw/search?keyword=%E5%86%B0%E7%AE%B1',
                'content-type':'application/json; charset=utf-8',
                'cookie':'_fbp=fb.1.1593007036899.1842863687; SPC_F=D6b67L9ek5gJ2K61Twdq6jMEsfcCVTPQ; REC_T_ID=9daa2992-b622-11ea-a175-b49691276970; __BWfp=c1593007142596x78a882006; csrftoken=ZyrUL8EJJXXf3DyEfTS1cqdjjOcPEHjZ; welcomePkgShown=true; G_ENABLED_IDPS=google; SPC_CLIENTID=RDZiNjdMOWVrNWdKrbzgclqjtcqheebv; SPC_IA=-1; SPC_EC=-; SPC_U=-; _fbc=fb.1.1609918057362.IwAR1pchvBVbRoEvcP6uZ7jOBuebY2WTvPanh9y37m9UmwDGkVzO5cozlV1Ak; _gcl_au=1.1.1500884965.1610285194; _med=refer; SPC_SI=mall.AckngXLbRaGZGJe6bkdN4ksyN8jwLq09; _gid=GA1.2.1986988950.1611814039; SPC_SC_UD=; UYOMAPJWEMDGJ=; SPC_SC_TK=; SC_DFP=W684bVqB6lPJaGTk37ggLw292va0FtdF; AMP_TOKEN=%24NOT_FOUND; SPC_CT_acdd70d3="1611820641.yGNcw0YgxfG1ZsmR5ruOQGsnnReJ4KlatAmp2hbzFZc="; SPC_CT_178a2577="1611820977./TiRVPYlhNcD6VcyBspXmttWdpaBnt55ZPosTnLFS+4="; SPC_CT_69e08d42="1611821787.fGOSLVJuIKWmXwHDmKS/YXs351pE4nikIoj35proIao="; _ga_RPSBE3TQZZ=GS1.1.1611819635.12.1.1611821787.0; _ga=GA1.1.2118555010.1593007038; _dc_gtm_UA-61915057-6=1; SPC_R_T_ID="2fqmSqPVABGrrsRUTtXmmcYoiZO2As2lDZZ8PASNXF3ZLBF+Jog0hgdmRHA38Tv6V6jTHE1teaaliVDS2hEPB6JpdKkgyjaSrjntlr1kD1Y="; SPC_T_IV="WjRo63N3RYwDP4r6w8fDYw=="; SPC_R_T_IV="WjRo63N3RYwDP4r6w8fDYw=="; SPC_T_ID="2fqmSqPVABGrrsRUTtXmmcYoiZO2As2lDZZ8PASNXF3ZLBF+Jog0hgdmRHA38Tv6V6jTHE1teaaliVDS2hEPB6JpdKkgyjaSrjntlr1kD1Y="',
                }
            url = f'https://shopee.tw/api/v2/search_items/?by=relevancy&keyword={self.product_name}&limit=20&newest=0&order=desc&page_type=search&version=2'
            res = requests.get(url, headers = headers)
            reqsjson = json.loads(res.text)
            items = reqsjson.get('items')
            
            for item in items:
                title = item['name']
                shopid = item['shopid']
                itemid = item['itemid']
                titleWeb = title.replace(' ','-').replace('/','-')
                link = 'https://shopee.tw/{titleWeb}-i.{shopid}.{itemid}'.format(titleWeb=titleWeb, shopid=shopid, itemid=itemid)
                # link = 'https://shopee.tw/{titleWeb}-i.{shopid}.{itemid}'.format(titleWeb=titleWeb, shopid=shopid, itemid=itemid)
                hist_sold = item['historical_sold']
                # price = str(item['price'])[:-5]

                if item['price_before_discount'] == 0 :
                    price_before = str(item['price'])[:-5]
                    price = '-'
                    # print('售價:', price)
                else:
                    price_min_before = item['price_before_discount']
                    price_min = item['price_min']
                    price_max_before = item['price_max_before_discount']
                    price_max = item['price_max']
                    if price_max == price_min:
                        price_before = str(price_min_before)[:-5]
                        price = str(price_min)[:-5]
                        # print('售價:', str(price_min_before)[:-5])
                        # print('特價:', str(price_min)[:-5])
                    
                    else:            
                        price_min_range = str(price_min_before)[:-5] + '~' + str(price_max_before)[:-5]
                        price_max_range = str(price_min)[:-5] + '~' + str(price_max)[:-5]
                        price_before = price_min_range
                        price = price_max_range  
                        # print('售價:', price_min_range)
                        # print('特價:', price_max_range)           
                
                loaction = item['shop_location']
                star = round(item['item_rating']['rating_star'],1)    
                result.append(dict(title=title, link=link, hist_sold=hist_sold, price_before=price_before ,price=price, loaction=loaction, star=star))

        return result

            
