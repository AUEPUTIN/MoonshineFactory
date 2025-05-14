import os
import django
from djangoProject2 import settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE","djangoProject1.settings")
django.setup()
from django.contrib.admin.sites import site
from django.db.models.fields.files import ImageFieldFile
from bar.admin import (
    AboutPageAdmin,
    ProductAdmin,
    CocktailAdmin,
    IngredientAdmin,
    ContactInfoAdmin,
)
from django.test import TestCase
from django.core.exceptions import ValidationError
from bar.models import Cocktail, Ingredient, AboutPage, Product, CocktailIngredient, ContactInfo
from django.urls import resolve, reverse
from bar.views import (
    AboutPageView, ProductListView, ProductDetailView,
    CocktailListView, CocktailDetailView, ContactPageView
)

def get_image():
    rel_path = 'test_img/test.jpg'
    full_path = os.path.join(settings.MEDIA_ROOT, rel_path)
    return ImageFieldFile(instance=None, field=Product._meta.get_field('image'), name=rel_path)
# ------------------ View classes tests ------------------

class ViewTests(TestCase):

# about page tests

    def test_get_object(self):
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Про Ukrainian Spirit")
        self.assertContains(response, "Ukrainian Spirit — це не просто напої. Це філософія, культура, і любов до українських традицій. Ми створюємо автентичні смаки, які розповідають історію України кожному, хто їх скуштує.")

# product page tests

    def test_get_queryset_with_filters(self):
        image = get_image()
        product1 = Product.objects.create(name="Vodka",
                                          category="spirit",
                                          abv=40.0,
                                          volume="0.7L",
                                          image=image,
                                          is_kosher=True,
                                          is_limited=False)
        product2 = Product.objects.create(name="Whisky",
                                          category="spirit",
                                          abv=43.0,
                                          volume="0.7L",
                                          image=image,
                                          is_kosher=False,
                                          is_limited=False)
        response = self.client.get('/products/?name=Vodka')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, product1.name)
        self.assertNotContains(response, product2.name)

    def test_context_in_template_for_product(self):
        image = get_image()
        product = Product.objects.create(name="Rum",
                                         category="spirit",
                                         abv=37.5,
                                         volume="0.7L",
                                         image=image,
                                         is_kosher=True,
                                         is_limited=False)
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('products', response.context)
        self.assertIn(product, response.context['products'])

# product detail page tests

    def test_get_product_detail(self):
        image = get_image()
        product = Product.objects.create(name="Gin",
                                         description="Distilled spirit",
                                         category="spirit",
                                         abv=40.0,
                                         volume="0.7L",
                                         image=image,
                                         is_kosher=True,
                                         is_limited=False)
        response = self.client.get(f'/products/{product.pk}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, product.name)
        self.assertContains(response, product.description)
        self.assertIn('product', response.context)
        self.assertEqual(response.context['product'], product)

# cocktail list page tests

    def test_get_queryset_with_query(self):
        image = get_image()
        cocktail1 = Cocktail.objects.create(name="Mojito", description="Refreshing drink", image=image)
        cocktail2 = Cocktail.objects.create(name="Margarita", description="Classic cocktail", image=image)
        response = self.client.get('/cocktails/?q=Mojito')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, cocktail1.name)
        self.assertNotContains(response, cocktail2.name)

    def test_context_in_template_for_cocktail(self):
        image = get_image()
        cocktail = Cocktail.objects.create(name="Negroni", description="Bitter and sweet", image=image)
        response = self.client.get('/cocktails/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('cocktails', response.context)
        self.assertIn(cocktail, response.context['cocktails'])

# cocktail detail page tests

    def test_get_cocktail_detail(self):
        image = get_image()
        cocktail = Cocktail.objects.create(name="Margarita", description="Classic cocktail", image=image)
        response = self.client.get(f'/cocktails/{cocktail.pk}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, cocktail.name)
        self.assertContains(response, cocktail.description)
        self.assertIn('cocktail', response.context)
        self.assertEqual(response.context['cocktail'], cocktail)

# contact page tests

    def test_get_contact_page(self):
        response = self.client.get('/contacts/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "м. Київ, вул. Хрещатик, 10")
        self.assertContains(response, "+380441234567")
        self.assertContains(response, "info@ukrainianspirit.ua")


# ------------------ urls tests ------------------

class URLTests(TestCase):
    def test_about_url(self):
        url = reverse('bar:about')
        self.assertEqual(resolve(url).func.view_class, AboutPageView)

    def test_product_list_url(self):
        url = reverse('bar:product_list')
        self.assertEqual(resolve(url).func.view_class, ProductListView)

    def test_product_detail_url(self):
        product = Product.objects.create(name="Vodka", category="h", abv=40.0, volume="0.7L")
        url = reverse('bar:product_detail', args=[product.pk])
        self.assertEqual(resolve(url).func.view_class, ProductDetailView)

    def test_cocktail_list_url(self):
        url = reverse('bar:cocktail_list')
        self.assertEqual(resolve(url).func.view_class, CocktailListView)

    def test_cocktail_detail_url(self):
        cocktail = Cocktail.objects.create(name="Mojito", description="...")
        url = reverse('bar:cocktail_detail', args=[cocktail.pk])
        self.assertEqual(resolve(url).func.view_class, CocktailDetailView)

    def test_contacts_url(self):
        url = reverse('bar:contacts')
        self.assertEqual(resolve(url).func.view_class, ContactPageView)



class ProjectURLTests(TestCase):
    def test_index_url(self):
        resolver = resolve('/')
        self.assertEqual(resolver.func.__name__, 'index')

    def test_admin_url(self):
        resolver = resolve('/admin/')
        self.assertEqual(resolver.func.__module__, 'django.contrib.admin.sites')

    def test_include_bar_urls(self):
        # Перевірка, що /about/ працює як наслідок include('bar.urls')
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)
