from django.db import models
from bs4 import BeautifulSoup as bs
from datetime import datetime
import requests

# Create your models here.
class shopee:
    def __int__(self, product_name):
        self.product_name = product_name

    def scrape(self):
        result = []

        if self.product_name:
            resp = requests.get(f'https://shopee.tw/api/v2/search_items/?by=relevancy&keyword={self.product_name}&limit=20&newest=0&order=desc&page_type=search&version=2')
            items = resp.json['items']
        return items

            
