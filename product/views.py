from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Product
from django.http import JsonResponse

@login_required
def index(request):
    return render(request, 'product/product.html')
    # return HttpResponse("Hello, world. You're at the product index.")


@login_required
def ajax_product_count(request):
    prod_id = request.POST.get('prod_id')
    res = Product.objects.values('qty').filter(id=prod_id)
    if res:
        data = {
            'quantity': res[0]['qty']
        }
    else:
        data = {
            'err': "Error Occurred"
        }
    return JsonResponse(data)
