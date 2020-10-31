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

    path('admin_panel/', views.admin_panel, name="admin_panel"),
    path('create_product_form/', views.create_product_form, name="create_product_form"),
    path('edit_product_form/<int:id>/', views.edit_product_form, name="edit_product_form")
]
