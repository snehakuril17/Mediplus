"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from myapp import views

urlpatterns = [
      path('admin/', admin.site.urls),
      path('', views.index),
      path('signup', views.signup),
      path('insert', views.insertdata),
      path('signin', views.signin),
      path('verifyuser',views.verifyuser),
      path('shop',views.shop),
      path('logout',views.logout),
      path('details/<int:pid>',views.prodetails),
      path('userdata',views.userdata),
      path('update', views.update),
      path('editprofile',views.editprofile),
      path('cart',views.showcart),
      path('addproduct',views.insertcart),
      path('remove/<int:rid>',views.removecartiteam),
      path('increase/<int:iid>',views.increase),
      path('decrease/<int:did>',views.decrease),
      path('placeorder',views.placeorder),
      path('paymentsuccess',views.payment_success),
      path('manageorder',views.manageorder),
      path('orderdetails/<int:oid>',views.orderdetails),
      path('categoryproducts', views.filter_products, name='category_products'),
      path('productsearch', views.productsearch, name='productsearch'),
      path('contact',views.contactdata),
      path('contactdata',views.contactMessage),
      path('about',views.about),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
