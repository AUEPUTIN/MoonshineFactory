from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import (
    AboutPage, Product, Cocktail,
    Ingredient, CocktailIngredient, ContactInfo
)

def index(request):
    return render(request, 'index.html')


# --- AboutPage ---
class AboutPageView(DetailView):
    model = AboutPage
    template_name = 'bar/about.html'
    context_object_name = 'about'

    def get_object(self):
        # Завжди віддаємо AboutPage з pk=1
        return AboutPage.objects.first()


# --- Product ---
class ProductListView(ListView):
    model = Product
    template_name = 'bar/products.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name', '')
        category = self.request.GET.get('category', '')
        volume = self.request.GET.get('volume', '')
        is_kosher = self.request.GET.get('is_kosher', '')
        is_limited = self.request.GET.get('is_limited', '')

        # Фільтрація за кожним полем
        if name:
            queryset = queryset.filter(name__icontains=name)
        if category:
            queryset = queryset.filter(category__icontains=category)
        if volume:
            try:
                volume_value = float(volume)
                queryset = queryset.filter(volume=volume_value)
            except ValueError:
                pass  # Якщо введено некоректне значення, просто ігноруємо
        if is_kosher:
            queryset = queryset.filter(is_kosher=is_kosher.lower() == 'true')
        if is_limited:
            queryset = queryset.filter(is_limited=is_limited.lower() == 'true')

        return queryset


class ProductDetailView(DetailView):
    model = Product
    template_name = 'bar/product_detail.html'
    context_object_name = 'product'


# --- Cocktail ---
from django.views.generic import ListView
from .models import Cocktail
from django.db.models import Q

class CocktailListView(ListView):
    model = Cocktail
    template_name = 'bar/cocktails.html'
    context_object_name = 'cocktails'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(name__icontains=query)
        return queryset



class CocktailDetailView(DetailView):
    model = Cocktail
    template_name = 'bar/cocktail_detail.html'
    context_object_name = 'cocktail'

# --- ContactInfo ---
class ContactPageView(DetailView):
    model = ContactInfo
    template_name = 'bar/contacts.html'
    context_object_name = 'contact'

    def get_object(self):
        return ContactInfo.objects.first()

