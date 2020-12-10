"""CRM URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url

from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from user import views as core_views
from product import views as product_views
from order import views as order_views

from django.conf import settings
from django.conf.urls.static import static


admin.site.site_header = "Steadfast Admin"
admin.site.site_title = "Steadfast Admin Portal"
admin.site.index_title = "Welcome to Steadfast Nutrition Portal"

# from order.views import (HomepageView, OrderUpdateView, CreateOrderView, delete_order,
#                           OrderListView, done_order_view, auto_create_order_view,
#                           ajax_add_product, ajax_modify_order_item, ajax_search_products, ajax_calculate_results_view,
#                           order_action_view, ajax_calculate_category_view
#                           )

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^order/$', order_views.index, name='order'),
    url(r'^previous_order/$', order_views.previous_order, name="previous_order"),
    url(r'^order_details/$', order_views.order_details, name="order_details"),
    url(r'^$', order_views.place_order, name="home"),
    url(r'^place_final_order/$', order_views.place_final_order, name="place_final_order"),
    url(r'^order_confirm/$', order_views.order_confirm, name="order_confirm"),
    url(r'^login/$', core_views.login_user, name="login"),
    url(r'^logout/$', core_views.logout, name='logout'),
    url(r'^signup/$', core_views.signup, name='signup'),
    path('sent/', core_views.activation_sent_view, name="activation_sent"),
    path('activate/<slug:uidb64>/<slug:token>/', core_views.activate, name='activate'),

    # ajax_calls
    url(r'^ajax/update-cart/$', order_views.ajax_update_cart, name='update-cart'),
    url(r'^ajax/product-count/$', product_views.ajax_product_count, name='product-count'),


    # path('', HomepageView.as_view(), name='homepage'),
    # path('order1-list/', OrderListView.as_view(), name='order_list'),
    # path('create/', CreateOrderView.as_view(), name='create-order1'),
    # path('create-auto/', auto_create_order_view, name='create_auto'),
    # path('update/<int:pk>/', OrderUpdateView.as_view(), name='update_order'),
    # path('done/<int:pk>/', done_order_view, name='done_order'),
    # path('delete/<int:pk>/', delete_order, name='delete_order'),
    # path('action/<int:pk>/<slug:action>/', order_action_view, name='order_action'),


    #  ajax_calls
    # path('ajax/search-products/<int:pk>/', ajax_search_products, name='ajax-search'),
    # path('ajax/add-product/<int:pk>/<int:dk>/', ajax_add_product, name='ajax_add'),
    # path('ajax/modify-product/<int:pk>/<slug:action>', ajax_modify_order_item, name='ajax_modify'),
    # path('ajax/calculate-results/', ajax_calculate_results_view, name='ajax_calculate_result'),
    # path('ajax/calculate-category-results/', ajax_calculate_category_view, name='ajax_category_result'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
