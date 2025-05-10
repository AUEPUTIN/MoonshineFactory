from django.contrib import admin
from django.utils.html import format_html
from .models import AboutPage

@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'image_tag')
    readonly_fields = ('image_tag',)

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="150" />', obj.image.url)
        return "-"
    image_tag.short_description = 'Зображення'

from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'abv', 'volume', 'is_kosher', 'is_limited', 'image_tag')
    list_filter = ('category', 'is_kosher', 'is_limited')
    search_fields = ('name', 'description')
    readonly_fields = ('image_tag',)

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" />', obj.image.url)
        return "-"
    image_tag.short_description = 'Зображення'

from .models import Cocktail, Ingredient, CocktailIngredient

class CocktailIngredientInline(admin.TabularInline):
    model = CocktailIngredient
    extra = 1

@admin.register(Cocktail)
class CocktailAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_tag')
    search_fields = ('name', 'description')
    inlines = [CocktailIngredientInline]
    readonly_fields = ('image_tag',)

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" />', obj.image.url)
        return "-"
    image_tag.short_description = 'Зображення'

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

from .models import ContactInfo

@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('address', 'phone', 'email')
    search_fields = ('address', 'email')