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
    path('developer/', views.developer, name="developer")
]
