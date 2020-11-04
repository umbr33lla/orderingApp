
#Django imports

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.http import JsonResponse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.urls import resolve

#Local imports

from .models import *
from .forms import CreateUserForm, CreateCustomerForm, CreateProductForm
from .decorators import unauthenticated_user, allowed_users, admin_only
from .filters import ProductFilter, CustomerFilter

import json
import datetime

@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='customer')
            user.groups.add(group)

            messages.success(request, 'Account was created for ' + username)
            return redirect('login')

    context = {'form': form}
    return render(request, 'accounts/register.html', context)


@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or password is incorrect!')
    context = {}
    return render(request, 'accounts/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@admin_only
def home(request):

    totalProducts = Product.objects.all().count()
    totalCustomers = Customer.objects.all().count()
    totalCompletedOrders = Order.objects.filter(complete__iexact=True).count()
    totalInompletedOrders = Order.objects.filter(complete__iexact=False).count()

    context = {
        'totalProducts': totalProducts, 
        'totalCustomers': totalCustomers, 
        'totalCompletedOrders': totalCompletedOrders,
        'totalInompletedOrders': totalInompletedOrders}

    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Product.objects.get_queryset().order_by('name')
    customers = Customer.objects.all()

    productFilter = ProductFilter(request.GET, queryset=products)
    products = productFilter.qs

    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')

    try:
        products = paginator.page(page_number)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    context = {'products': products, 'customers': customers,
               'productFilter': productFilter, 'paginator': paginator}

    return render(request, 'accounts/product.html', context)


@login_required(login_url='login')
def cart(request, id):
    customer = Customer.objects.get(id=id)
    customerId = customer.id
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)

    items = order.orderitem_set.get_queryset().order_by('id')

    cart_items = order.get_cart_items
    context = {"customer": customer, "customerId": customerId, 'items': items,
               'order': order, 'cartItems': cart_items}
    return render(request, 'accounts/cart.html', context)


def customer_order(request):
    context = {}
    return render(request, 'accounts/customer_order.html', context)


def update_item(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customerQs = data['customer']
    customer = Customer.objects.get(id=customerQs)

    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(
        order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Success', safe=False)


def process_order(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    customerQs = data['customer']
    customer = Customer.objects.get(id=customerQs)
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)

    total = float(data['total'])
    order.transaction_id = transaction_id

    if total == float(order.get_cart_total):
        order.complete = True
    order.save()

    return JsonResponse('Order complete!', safe=False)


def product_form(request):

    products = Product.objects.get_queryset().order_by('name')

    productFilter = ProductFilter(request.GET, queryset=products)
    products = productFilter.qs
    
    productPaginator = Paginator(products, 10)
    product_page_number = request.GET.get('page')

    try:
        products = productPaginator.page(product_page_number)
    except PageNotAnInteger:
        products = productPaginator.page(1)
    except EmptyPage:
        products = productPaginator.page(productPaginator.num_pages)

    context = { 'products': products, 'productFilter': productFilter}

    return render(request, 'accounts/product_template.html', context)



def create_product(request):
    formProduct = CreateProductForm()

    if request.method == 'POST':
        form = CreateProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully saved!')
            return redirect('product_form')

    context = { 'formProduct': formProduct }
    return render(request, 'accounts/product_form.html', context)



def update_product(request, id):

    product = Product.objects.get(id=id)
    formProduct = CreateProductForm(instance=product) 


    if request.method == 'POST':
        form = CreateProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated!')
            return redirect('product_form')

    context = { 'formProduct': formProduct}
    return render(request, 'accounts/product_form.html', context)



def customer_form(request):
     customers = Customer.objects.get_queryset().order_by('name')

     customerFilter = CustomerFilter(request.GET, queryset=customers)

     customers = customerFilter.qs

     customerPaginator = Paginator(customers, 10)
     customer_page_number = request.GET.get('page')

     try:
        customers = customerPaginator.page(customer_page_number)
     except PageNotAnInteger:
        customers = customerPaginator.page(1)
     except EmptyPage:
        customers = customerPaginator.page(customerPaginator.num_pages)

     context = { 'customers': customers, 'customerFilter': customerFilter}

     return render(request, 'accounts/customer_template.html', context)



def update_customer(request, id):

    customer = Customer.objects.get(id=id)
    formCustomer = CreateCustomerForm(instance=customer) 

    if request.method == 'POST':
        form = CreateCustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer_form')

    context = { 'formCustomer': formCustomer}

    return render(request, 'accounts/customer_form.html', context)










