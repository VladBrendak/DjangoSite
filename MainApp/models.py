from distutils.command.upload import upload
from email.policy import default
from pyexpat import model
from django.db import models
from django.forms import CharField, ImageField, FileField
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.contrib.auth.models import  User

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, blank=True)
    nickname = models.CharField(max_length=35, unique=False, blank=True) # unique=True
    slug = models.SlugField(max_length=255, db_index = True)
    username = models.CharField(max_length=30, blank=True)
    surname = models.CharField(max_length=30, blank=True)
    avatar_photo = models.ImageField(upload_to="photos/", default='photos/user_avatar.png')
    email = models.EmailField(max_length=255, blank=True, null = True)
    is_creator = models.BooleanField(default=False)
    card_number = models.CharField(max_length=29, blank=True)
    creator_nickname = models.CharField(max_length=35, blank=True, unique=False) #unique=True
    creator_phone_number = models.CharField(max_length=25, blank=True)
    creator_email = models.EmailField(max_length=255, blank=True, unique=False) #unique = True

    def __str__(self):
        return self.nickname

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.username)
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ['id']

class Product(models.Model):
    product_title = models.CharField(max_length=50)
    product_fullname = models.CharField(max_length=255)
    product_slug = models.SlugField(max_length=255, db_index = True)
    product_description = models.TextField()
    product_price = models.DecimalField(max_digits=6, decimal_places=2)
    product_file = models.FileField(upload_to='ProductFiles/', default='photos/user_avatar.png')
    title_image = models.ImageField(upload_to='photos/', default='photos/user_avatar.png')
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey('Customer', null=True, on_delete=models.PROTECT)

    def __str__(self):
        return self.product_title

    def get_absolute_url(self):
        return reverse('product_page', kwargs={'product_id' : self.pk, 'product_slug' : self.product_slug})

    def save(self, *args, **kwargs):
        if not self.product_slug:
            self.product_slug = slugify(self.product_fullname)
        return super().save(*args, **kwargs)


    class Meta:
        ordering = ['id']

class ProductImages(models.Model):
    image = models.ImageField(upload_to='photos/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    

class Cart(models.Model):
    user = models.ForeignKey('Customer', on_delete=models.SET_NULL, blank=True, null=True)
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    product = models.ForeignKey('Product', on_delete=models.PROTECT, null=True)
    comment_nickname = models.CharField(max_length=35)
    comment_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Discount(models.Model):
    disc_name = models.CharField(max_length=50)
    disc_description = models.TimeField()
    disc_percent = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

class Discount_of_product(models.Model):
    discount = models.ForeignKey('Discount', on_delete=models.PROTECT)
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

class Order_details(models.Model):
    is_paid = models.BooleanField(default=False)
    user = models.ForeignKey('Customer', on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    @property
    def get_cart_total(self):
        orderitems = self.order_items_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.order_items_set.all()
        total = len(orderitems)
        return total

class Order_items(models.Model):
    order = models.ForeignKey('Order_details', on_delete=models.SET_NULL, blank=True, null=True)
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    @property
    def get_total(self):
        total = self.product.product_price
        return total