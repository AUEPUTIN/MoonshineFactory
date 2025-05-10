from django.urls import path
from .views import (
    AboutPageView,
    ProductListView, ProductDetailView,
    CocktailListView, CocktailDetailView,
    ContactPageView
)

app_name = 'bar'

urlpatterns = [

    # Головна сторінка "Про нас"
    path('about/', AboutPageView.as_view(), name='about'),

    # Продукти
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),

    # Коктейлі
    path('cocktails/', CocktailListView.as_view(), name='cocktail_list'),
    path('cocktails/<int:pk>/', CocktailDetailView.as_view(), name='cocktail_detail'),

    # Контакти
    path('contacts/', ContactPageView.as_view(), name='contacts'),
]
