from email import message
from http.client import HTTPResponse
from string import Template
from turtle import title
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, JsonResponse
import json
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, CreateView
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .forms import *
from .decorators import *
from .models import *
from .utils import *

# Create your views here.

def home(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order_details.objects.get_or_create(user=customer, is_paid=False)
        items = order.order_items_set.all()
        cartItems = order.get_cart_items
    else:
        items = ['get_cart_items']
        order = {'get_cart_total' : 0, 'get_cart_items' : 0}
        cartItems = order
        

    context = { 'navMenu' : navMenu,
                'title' : 'Home',
                'cartItems' : cartItems}

    return render(request, 'MainApp/Home.html', context=context)

# ----------------------------------------------------------------------------------------------

def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order_details.objects.get_or_create(user=customer, is_paid=False)
        items = order.order_items_set.all()
        cartItems = order.get_cart_items
    else:
        items = ['get_cart_items']
        order = {'get_cart_total' : 0, 'get_cart_items' : 0}
        cartItems = order
       
    products = Product.objects.all()
    paginator = Paginator(products, 12)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = { 'navMenu' : navMenu,
                'title' : 'Store',
                'products': products,
                'page_obj' : page_obj,
                'cartItems' : cartItems}

    return render(request, 'MainApp/ShopFake.html', context=context)

# ----------------------------------------------------------------------------------------------


def novelties(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order_details.objects.get_or_create(user=customer, is_paid=False)
        items = order.order_items_set.all()
        cartItems = order.get_cart_items
    else:
        items = ['get_cart_items']
        order = {'get_cart_total' : 0, 'get_cart_items' : 0}
        cartItems = order

    users = Customer.objects.all().filter(is_creator = True)
    paginator = Paginator(users, 12)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    products = Product.objects.all().order_by('-created_at')[:3]
    context = { 'navMenu' : navMenu,
                'title' : 'Novelties',
                'products': products,
                'autors': users,
                'page_obj' : page_obj,
                'cartItems' : cartItems}

    return render(request, 'MainApp/NoveltiesFake.html', context=context)
    
# ----------------------------------------------------------------------------------------------


def product_page(request, product_id, product_slug):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order_details.objects.get_or_create(user=customer, is_paid=False)
        items = order.order_items_set.all()
        cartItems = order.get_cart_items
    else:
        items = ['get_cart_items']
        order = {'get_cart_total' : 0, 'get_cart_items' : 0}
        cartItems = order

    product = get_object_or_404(Product, pk = product_id)
    images = ProductImages.objects.select_related().filter(product = product_id)
    comments = Comment.objects.select_related().filter(product = product_id).order_by('-created_at')

    form = CreateCommentForm()

    if request.method == 'POST':
        form = CreateCommentForm(request.POST)
        if form.is_valid():
            nickname = request.user.customer.nickname
            comment = form.save()
            comment.product = product
            comment.comment_nickname = nickname
            comment.save()
            form = CreateCommentForm()
            return HttpResponseRedirect(request.path_info)
        else:
            form = CreateCommentForm()

    context = { 'navMenu' : navMenu,
                'title': 'product_page',
                'product' : product,
                'images' : images,
                'form':form,
                'comments': comments,
                'cartItems' : cartItems}

    return render(request, 'MainApp/product_page.html', context=context)

# ----------------------------------------------------------------------------------------------

# @allowed_users(allowed_roles=['admin'])
def add_product(request):
    form = AddProductForm()
    creator = request.user.customer
    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES)
        images = request.FILES.getlist('images')
        
        if form.is_valid():

            if len(images) <= 3 and len(images) >=1:
                product = form.save()
                for image in images:
                    product.creator = creator
                    product.save()
                    photo = ProductImages.objects.create(image=image, product=product)
                return redirect('shop')
            else:
                messages.info(request, 'There must be 3 images!!! images finded: ' + str(len(images)))
        else:
            form = AddProductForm()

    context = { 'navMenu' : navMenu,
                'title': 'add_product',
                'form': form}

    return render(request, 'MainApp/add_product.html', context=context)


# ----------------------------------------------------------------------------------------------

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer', 'admin'])
def user_page(request):
    customer = request.user.customer
    form = UserCustomerForm(instance=customer)
    if request.method == 'POST':
        form = UserCustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            form = UserCustomerForm(request.FILES, instance=customer)

    context = { 'form' : form,
                'navMenu' : navMenu,
                'title': 'user_page'}

    return render(request, 'MainApp/User_page.html', context=context)

@unautheficated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR Password is incorrect !!!')

    context = { 'navMenu' : navMenu,
                'title' : 'login'}

    return render(request, 'MainApp/Login.html',  context=context)


def logoutUser(request):
    logout(request)
    return redirect('login')

@unautheficated_user
def registerPage(request):
    form = CreateUserForm()
    
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            customer = Customer(user=user, nickname=user.username, email=user.email)
            customer.save()
            return redirect('login')

    context = { 'form': form,
                'navMenu' : navMenu,
                'title' : 'register'}

    return render(request, 'MainApp/Register.html',  context=context)

def BecomeCreator(request):
    customer = request.user.customer
    form = BecomeCreatorForm(instance=customer)

    if request.method == 'POST':
        form = BecomeCreatorForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            form = BecomeCreatorForm(instance=customer)
            messages.info(request, 'You should confirm all privacy and policy')

    context = { 'navMenu' : navMenu, 'title' : 'Become a creator', 'form' : form}

    return render(request, 'MainApp/BecomeCreator.html',  context=context)

@login_required(login_url='login')
def CartPage(request):
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order_details.objects.get_or_create(user=customer, is_paid=False)
        items = order.order_items_set.all()
    else:
        items = []
        order = {'get_cart_total' : 0, 'get_cart_items' : 0}

    context = { 'navMenu' : navMenu, 'title' : 'Cart', 'items' : items, 'order' : order}

    return render(request, 'MainApp/Cart_page.html',  context=context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order_details.objects.get_or_create(user=customer, is_paid=False)
        items = order.order_items_set.all()
    else:
        items = []
        order = {'get_cart_total' : 0, 'get_cart_items' : 0}

    context = { 'navMenu' : navMenu, 'title' : 'Cart', 'items' : items, 'order' : order}

    return render(request, 'MainApp/Checkout_page.html',  context=context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('ProductId', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order_details.objects.get_or_create(user=customer, is_paid=False)

    orderItem, created = Order_items.objects.get_or_create(order=order, product=product)

    orderItem.save()

    if action == 'remove':
        orderItem.delete()

    return JsonResponse('Item just added', safe=False)

def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1> Page Not Found !!! 404 </h1>")