from django.shortcuts import render

# Create your views here.
from .models import Order, OrderItem
from product.models import Category, Product
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
    order_items = OrderItem.objects.filter(order_id=order_uuid).select_related('product')
    print(order_items.query)

    return render(request, 'order/order-details.html', {'order_data': order_items})


@login_required
def previous_order(request):
    prev_order = Order.objects.all()
    print('ordr data', prev_order)
    return render(request, 'order/previous-page.html', {'order_data':prev_order})
    # return HttpResponse("Hello, world. You're at the product index.")


@login_required
def place_order(request):
    categories = Category.objects.all()
    product_template_str = ''
    for cat in categories:
        product_template_str += '<th>' + cat.title + '</th>'
        products = Product.objects.filter(category_id=cat.id)
        for prod in products:
            product_template_str += '<tr><td>' + prod.title + '</td>'
            product_template_str += '<td>' + prod.flavour + '</td>'
            product_template_str += '<td>' + str(prod.value) + '</td>'
            product_template_str += '<td><div class="input-group"><input type="button" value="-" class="button-minus" data-field="quantity"><input type="number" step="1" max="" value="1" name="quantity" class="quantity-field"><input type="button" value="+" class="button-plus" data-field="quantity"></div></td>'
            product_template_str += '</tr>'

    # product = Product.objects.all()
    print('product_template_str', product_template_str)
    return render(request, 'order/order-place.html', {'product_template': product_template_str})
