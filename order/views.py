from django.shortcuts import render

# Create your views here.
from .models import Order
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    order_data = Order.objects.all()
    print('ordr data', order_data)
    return render(request, 'order/table-basic.html', {'order_data':order_data})
    # return HttpResponse("Hello, world. You're at the product index.")


@login_required
def previous_order(request):
    prev_order = Order.objects.all()
    print('ordr data', prev_order)
    return render(request, 'order/previous-page.html', {'order_data':prev_order})
    # return HttpResponse("Hello, world. You're at the product index.")


@login_required
def place_order(request):
    return render(request, 'order/order-place.html')
    # return HttpResponse("Hello, world. You're at the product index.")