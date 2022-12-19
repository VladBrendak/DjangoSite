from contextlib import nullcontext
from dataclasses import fields
from django.core.exceptions import ValidationError
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        # fields = '__all__'
        fields = ['id', 'product_title', 'product_fullname', 'product_description', 'product_price', 'product_file', 'title_image']
    
    def clean_product_title(self):
        product_title = self.cleaned_data['product_title']
        if len(product_title) > 25:
            raise ValidationError('number of symbols must be lower than 25! \n symbols given: ' + str(len(product_title)))

        return product_title


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserCustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user', 'slug', 'is_creator']

class BecomeCreatorForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['is_creator']

    def clean_is_creator(self):
        is_creator = self.cleaned_data['is_creator']
        if is_creator == False:
            raise ValidationError('You should confirm all privacy and policy to continue')

        return is_creator

class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_text']

        def clean_comment_text(self):
            comment_text = self.cleaned_data['comment_text']
            if len(comment_text) <= 0 and comment_text == None and comment_text == nullcontext:
                raise ValidationError('You should type something!')

            return comment_text