from django.shortcuts import render
from .models import shopee

# Create your views here.
def shopee(request):
    return render(request, 'shopee/shopee.html')