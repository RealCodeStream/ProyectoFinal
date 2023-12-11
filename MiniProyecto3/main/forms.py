from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Category, Product, Review, OrderHistory
#from django.shortcuts import kwargs

class CustomUserCreationForm(UserCreationForm):
    
    class Meta:
        model= User
        fields= ["username","email","password1","password2"]
        
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'description', 'price', 'image']
        
class ReviewForm(forms.Form):
    rating = forms.ChoiceField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], label='Calificación')
    comment = forms.CharField(widget=forms.Textarea, label='Comentario')
    
class OrderHistoryForm(forms.ModelForm):
    class Meta:
        model = OrderHistory
        fields = ['comment']