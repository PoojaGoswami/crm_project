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

from django.conf import settings
from django.conf.urls.static import static


# urlpatterns = [
#     path('product/', include('product.urls')),
#     path('order/', include('order.urls')),
#     path('athlete/', include('athlete.urls')),
#     path('admin/', admin.site.urls),
# ]

admin.site.site_header = "Steadfast Admin"
admin.site.site_title = "Steadfast Admin Portal"
admin.site.index_title = "Welcome to Steadfast Nutrition Portal"

from order.views import (HomepageView, OrderUpdateView, CreateOrderView, delete_order,
                         OrderListView, done_order_view, auto_create_order_view,
                         ajax_add_product, ajax_modify_order_item, ajax_search_products, ajax_calculate_results_view,
                         order_action_view, ajax_calculate_category_view
                         )

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', core_views.home, name='home'),
    url(r'^login/$', LoginView.as_view(template_name='user/login.html'), name='login'),
    url(r'^logout/$', core_views.logout, name='logout'),
    url(r'^signup/$', core_views.signup, name='signup'),

    # path('', HomepageView.as_view(), name='homepage'),
    # path('order-list/', OrderListView.as_view(), name='order_list'),
    # path('create/', CreateOrderView.as_view(), name='create-order'),
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
