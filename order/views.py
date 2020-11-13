from django.shortcuts import render, get_object_or_404

# Create your views here.
from .models import Order, OrderItem
from product.models import Category, Product
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse

from .cart import Cart

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
        products = Product.objects.filter(category_id=cat.id, active=1)
        for prod in products:
            product_template_str += '<tr><td>' + prod.title + '</td>'
            product_template_str += '<td>' + prod.flavour + '</td>'
            product_template_str += '<td>' + str(prod.value) + '</td>'
            product_template_str += '<td><div class="input-group"><input type="button" value="-" class="button-minus" data-field="quantity"><input type="number" onkeyUp="updateCart(this)" onchange="updateCart(this)" data-id="' + str(prod.id) + '" step="1" max="" value="0" name="quantity" class="quantity-field"><input type="button" value="+" class="button-plus" data-field="quantity"></div></td>'
            product_template_str += '</tr>'

    # product = Product.objects.all()
    # print('product_template_str', product_template_str)
    return render(request, 'order/order-place.html', {'product_template': product_template_str})


@login_required
def update_cart(request):
    prod_id = request.POST.get('prod_id')
    qty = request.POST.get('qty')
    print('hii', prod_id, qty)
    cart = Cart(request)
    product = get_object_or_404(Product, id=prod_id)
    cart.add(product=product, quantity=qty, update_quantity=True)


    # cart = Cart(request)
    # product = get_object_or_404(Product, id=prod_id)
    # cart.add(product=product, quantity=cd['quantity'], update_quantity=cd['update'])
    # return redirect('cart:cart_detail')

    data = {
        'updated': True
    }
    return JsonResponse(data)


@login_required
def place_final_order(request):
    return render(request, 'order/thankyou.html')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})




