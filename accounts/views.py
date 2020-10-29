from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.http import JsonResponse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .models import *
from .forms import CreateUserForm, CreateCustomerForm
from .decorators import unauthenticated_user, allowed_users, admin_only
from .filters import ProductFilter

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
    return render(request, 'accounts/dashboard.html')


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):

    products = Product.objects.get_queryset().order_by('name')
    customers = Customer.objects.all()

    productFilter = ProductFilter(request.GET, queryset=products)
    products = productFilter.qs

    paginator = Paginator(products, 5)
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

def developer(request):
    return render(request, 'accounts/developer.html')
