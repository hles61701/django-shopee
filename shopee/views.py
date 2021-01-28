from django.shortcuts import render
from .models import Shopee

# Create your views here.
def index(request):

    shopee = Shopee(request.POST.get('product_name'))
    context = {
        "shopees": shopee.scrape()
    }
    return render(request, 'shopee/index.html', context)