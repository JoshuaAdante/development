from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def product_list_view(request):
    return render(request, 'store/product_list.html')
