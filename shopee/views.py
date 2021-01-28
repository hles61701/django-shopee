from django.shortcuts import render

# Create your views here.
def shopee(request):
    return render(request, 'shopee/shopee.html')