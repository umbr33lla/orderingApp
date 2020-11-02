from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('product/', views.products, name="product"),
    path('cart/<int:id>/', views.cart, name="cart"),
    path('customer_order/', views.customer_order, name="customer_order"),
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('update_item/', views.update_item, name="update_item"),
    path('process_order/', views.process_order, name="process_order"),

    # Product Form

    path('product_form/', views.product_form, name="product_form"),
    path('create_product/', views.create_product, name="create_product"),
    path('update_product/<int:id>/', views.update_product, name="update_product"),

    # Customer Form

    path('customer_form/', views.customer_form, name="customer_form"),
    path('create_customer/', views.create_customer, name="create_customer"),
    path('update_customer/<int:id>/', views.update_customer, name="update_customer"),
]
