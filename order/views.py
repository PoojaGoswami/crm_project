from django.shortcuts import render, get_object_or_404

# Create your views here.
from .models import Order, OrderItem
from product.models import Category, Product
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse

from .cart import Cart
import datetime

from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
import logging


# Get an instance of a logger
logger = logging.getLogger(__name__)


@login_required
def index(request):
    current_user = request.user.id
    if request.user.is_superuser:
        order_data = Order.objects.all().select_related('user__profile')
    else:
        order_data = Order.objects.filter(user_id=current_user)
    # print(order_data.query)
    return render(request, 'order/table-basic.html', {'order_data': order_data})
    # return HttpResponse("Hello, world. You're at the product index.")


# @api_view(["GET"])
@login_required
def order_details(request):
    order_no = request.GET.get('order')
    order_items = OrderItem.objects.filter(order_id=order_no).select_related('product')
    # print(order_items.query)

    return render(request, 'order/order-details.html', {'order_data': order_items})


@login_required
def previous_order(request):
    current_user = request.user.id
    prev_order = Order.objects.filter(user_id=current_user)
    return render(request, 'order/previous-page.html', {'order_data':prev_order})


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
            product_template_str += '<td><div class="input-group"><input type="button" value="-" class="button-minus" data-field="quantity" data-id="' + str(prod.id) + '"><input type="number" onkeyUp="get_product_quantity(this, ' + "'manual'" + ')" onchange="get_product_quantity(this, ' + "'manual'" + ')" data-id="' + str(prod.id) + '" id="' + str(prod.id) + '" step="1" max="" value="0" name="quantity" class="quantity-field demoInput"><input type="button" value="+" class="button-plus" data-field="quantity" data-id="' + str(prod.id) + '"></div></td>'
            product_template_str += '</tr>'

    return render(request, 'order/order-place.html', {'product_template': product_template_str})


@login_required
def order_confirm(request):
    cart_session = request.session.get('cart')
    cart = Cart(request)
    print('len', cart.__len__())

    cart_template_str = ''
    for key, value in cart_session.items():
        prod_title = Product.objects.values_list('title', 'flavour').get(pk=key)
        cart_template_str += '<tr><td>' + prod_title[0] + '</td>'
        cart_template_str += '<td>' + prod_title[1] + '</td>'
        cart_template_str += '<td>' + value['final_price'] + '</td>'
        cart_template_str += '<td><div class="input-group"><input type="button" value="-" class="button-minus" data-field="quantity" data-id="' + key + '"><input type="number" onkeyUp="get_product_quantity(this, ' + "'manual'" + ')" onchange="get_product_quantity(this, ' + "'manual'" + ')" data-id="' + key + '" id="' + key + '" step="1" max="" value="' + value['quantity'] + '" name="quantity" class="quantity-field demoInput"><input type="button" value="+" class="button-plus" data-field="quantity" data-id="' + key + '"></div></td>'
        cart_template_str += '</tr>'

    return render(request, 'order/order-confirm.html', {'cart_template': cart_template_str})


@login_required
def ajax_add_product(request, pk, dk):
    instance = get_object_or_404(Order, id=pk)
    product = get_object_or_404(Product, id=dk)
    order_item, created = OrderItem.objects.get_or_create(order=instance, product=product)
    if created:
        order_item.qty = 1
        order_item.price = product.value
        order_item.discount_price = product.discount_value
    else:
        order_item.qty += 1
    order_item.save()
    product.qty -= 1
    product.save()
    instance.refresh_from_db()
    order_items = OrderItemTable(instance.order_items.all())
    RequestConfig(request).configure(order_items)
    data = dict()
    data['result'] = render_to_string(template_name='include/order_container.html',
                                      request=request,
                                      context={'instance': instance,
                                               'order_items': order_items
                                               }
                                    )
    return JsonResponse(data)


@login_required
def ajax_update_cart(request):
    prod_id = request.POST.get('prod_id')
    qty = request.POST.get('qty')
    # print('prod detail', prod_id, qty)
    cart = Cart(request)
    product = get_object_or_404(Product, id=prod_id)
    cart.add(product=product, quantity=qty, update_quantity=True)
    data = {
        'updated': True
    }
    return JsonResponse(data)


@login_required
def place_final_order(request):
    cart_session = request.session.get('cart')
    cart = Cart(request)
    ordered_items = cart.__iter__()
    print('len', cart.__len__())

    new_order = Order.objects.create(
        title='Order 66',
        date=datetime.datetime.now(),
        value=98,
        final_value=cart.get_total_final_price(),
        discount=cart.get_total_discount(),
        user_id=request.user.id,

    )
    new_order.title = f'Order - {new_order.id}'
    new_order.save()

    for key in cart_session:
        product = get_object_or_404(Product, id=key)
        order_item, created = OrderItem.objects.get_or_create(order_id=new_order.order_no, product_id=key)
        if created:
            order_item.qty = cart_session[key]['quantity']
            order_item.price = cart_session[key]['price']
            order_item.discount_price = cart_session[key]['discount']
        else:
            order_item.qty += 1
        order_item.save()
        product.qty -= int(cart_session[key]['quantity'])
        product.save()
        new_order.refresh_from_db()

    send_conformation_mail(request, new_order.order_no)

    del request.session['cart']

    return render(request, 'order/thankyou.html', {ordered_items: ordered_items})


def send_conformation_mail(request, order_no):
    cart_session = request.session.get('cart')

    email_subject = 'Order received'
    from_email = settings.EMAIL_HOST_USER
    to_email_list = [request.user.email, 'dm@steadfastnutrition.in', 'poojacs11@gmail.com']

    product_details = []
    for key, value in cart_session.items():
        prod_title = Product.objects.values_list('title', 'flavour').get(pk=key)
        prod_row = {'name': prod_title[0], 'flavour': prod_title[1], 'mrp': value['final_price'], 'quantity': value[
            'quantity']}
        product_details.append(prod_row)

    email_params = {'username': request.user.email,
                    'order_no': order_no,
                    'product_details': product_details}

    msg_plain = render_to_string('order/email_template.txt', email_params)
    msg_html = render_to_string('order/email_template.html', email_params)

    msg = EmailMultiAlternatives(email_subject, msg_plain, from_email, to_email_list)
    msg.attach_alternative(msg_html, "text/html")
    try:
        msg.send()
    except:
        logger.error("Unable to send mail.")


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})




