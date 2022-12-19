from django.contrib import admin

# Register your models here.

from .models import *

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_title', 'product_fullname', 'product_price', 'title_image', 'created_at', 'creator')

    prepopulated_fields = {'product_slug' : ("product_fullname",) }

admin.site.register(Product, ProductAdmin)

# class UserAdmin(admin.ModelAdmin):
#     list_display = (
#         'id',
#         'nickname',
#         'username',
#         'surname',
#         'avatar_photo',
#         'email',
#         'password',
#         'is_creator',
#         'card_number',
#         'creator_nickname',
#         'creator_phone_number',
#         'creator_email',
#         'date_joined',
#         'last_login',
#         'is_admin',
#         'is_active',
#         'is_staff',
#         'is_superuser',
#         )

    
#     readonly_fields = ('date_joined','last_login')

#     filter_horizontal = ()
#     list_filter = ()
#     fieldsets = ()

#     prepopulated_fields = {'slug' : ("nickname",) }

# admin.site.register(User, UserAdmin)


admin.site.register(Customer)

admin.site.register(ProductImages)

admin.site.register(Comment)

admin.site.register(Order_details)

admin.site.register(Order_items)