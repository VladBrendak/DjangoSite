
from unicodedata import name
from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('shop/', store, name='shop'),
    path('novelties/', novelties, name='novelties'),

    path('login/', loginPage, name='login'),
    path('register/', registerPage, name='register'),
    path('logout/', logoutUser, name='logout'),

    path('product/<int:product_id>/<slug:product_slug>/', product_page, name='product_page'),

    path('add_product/', add_product, name='add_product'),
    path('become_creator/', BecomeCreator, name='become_creator'),

    path('cart/', CartPage, name='cart'),
    path('checkout/', checkout, name='checkout'),
    path('update_item/', updateItem, name='update_item'),

    path('user/', user_page, name='user_page')]
