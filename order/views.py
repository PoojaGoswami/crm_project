from django.shortcuts import render

# Create your views here.
from .models import Order, OrderItem
from django.contrib.auth.decorators import login_required
import json

@login_required
def index(request):
    current_user = request.user.id
    print('current', current_user)
    order_data = Order.objects.filter(user_id=current_user)
    print('ordr data', order_data)
    return render(request, 'order/table-basic.html', {'order_data': order_data})
    # return HttpResponse("Hello, world. You're at the product index.")


# @api_view(["GET"])
@login_required
def order_details(request):
    current_user = request.user
    print('current', current_user)
    order_uuid = request.GET.get('order')

    # order_items = OrderItem.objects.filter(order_id=order_uuid)
    order_items = OrderItem.objects.filter(order_id=order_uuid).select_related('product')
    print(order_items.query)
    print('ordr data', order_items)

    return render(request, 'order/order-details.html', {'order_data': order_items})


@login_required
def previous_order(request):
    prev_order = Order.objects.all()
    print('ordr data', prev_order)
    return render(request, 'order/previous-page.html', {'order_data':prev_order})
    # return HttpResponse("Hello, world. You're at the product index.")


@login_required
def place_order(request):
    return render(request, 'order/order-place.html')
