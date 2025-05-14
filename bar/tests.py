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
# ------------------ Model classes tests ------------------

class ModelsTests(TestCase):
    # cocktail tests

    def test_cocktail_without_description(self):
        """Створення коктейлю без опису"""
        cocktail = Cocktail.objects.create(name="NoDescCocktail")
        self.assertEqual(cocktail.description, "")

    def test_cocktail_duplicate_name(self):
        """Можливо створити коктейлі з однаковим ім'ям (unique=False)"""
        c1 = Cocktail.objects.create(name="DuplicateName")
        c2 = Cocktail.objects.create(name="DuplicateName")
        self.assertNotEqual(c1.id, c2.id)

    def test_create_cocktail(self):
        """Перевіряє, чи можна створити коктейль із валідними даними"""
        cocktail = Cocktail.objects.create(
            name="Mojito",
            description="Mix mint and lime, add rum, top with soda.",
        )
        ingredients = [Ingredient.objects.create(name=name) for name in ["Mint", "Lime", "Rum", "Soda"]]
        cocktail.ingredients.set(ingredients)
        self.assertEqual(cocktail.name, "Mojito")
        self.assertEqual(cocktail.description, "Mix mint and lime, add rum, top with soda.")
        self.assertEqual(cocktail.ingredients.count(), 4)

    def test_str_method(self):
        """Перевіряє, чи метод __str__ повертає назву коктейлю"""
        cocktail = Cocktail.objects.create(
            name="Margarita",
            description="Shake with ice and strain into a glass."
        )
        ingredients = [Ingredient.objects.create(name=name) for name in ["Tequila", "Lime", "Triple Sec"]]
        cocktail.ingredients.set(ingredients)
        self.assertEqual(str(cocktail), "Margarita")

    def test_name_required(self):
        """Перевіряє, чи поле name є обов’язковим"""
        cocktail = Cocktail(description="Mix vodka and tonic.")
        with self.assertRaises(ValidationError):
            cocktail.full_clean()

    def test_empty_ingredients_and_description(self):
        """Перевіряє, чи поля ingredients і description можуть бути порожніми"""
        cocktail = Cocktail.objects.create(
            name="Simple Cocktail",
            description=""
        )
        self.assertEqual(cocktail.name, "Simple Cocktail")
        self.assertEqual(cocktail.ingredients.count(), 0)
        self.assertEqual(cocktail.description, "")

    def test_minimal_cocktail(self):
        """Перевіряє, чи можна створити коктейль лише з полем name"""
        cocktail = Cocktail.objects.create(name="Basic Cocktail")
        self.assertEqual(cocktail.name, "Basic Cocktail")
        self.assertEqual(cocktail.ingredients.count(), 0)
        self.assertEqual(cocktail.description, "")

# about page tests

    def test_about_page_with_empty_image(self):
        """Поле image може бути порожнім"""
        about = AboutPage.objects.create(title="No Image", content="No image here")
        self.assertFalse(about.image)

    def test_about_page_content_length(self):
        """content зберігається повністю"""
        long_content = "A" * 1000
        about = AboutPage.objects.create(title="Long Content", content=long_content)
        self.assertEqual(about.content, long_content)

    def test_create_about_page_and_str(self):
        about = AboutPage.objects.create(title="About Us", content="Info about the bar")
        self.assertEqual(about.title, "About Us")
        self.assertEqual(about.content, "Info about the bar")
        self.assertEqual(str(about), "About Us")

# product tests

    def test_product_kosher_and_limited(self):
        """Перевірка поєднання булевих полів"""
        product = Product.objects.create(name="Vodka", category="h", abv=37.5, is_kosher=False, is_limited=True)
        self.assertFalse(product.is_kosher)
        self.assertTrue(product.is_limited)

    def test_product_abv_type(self):
        """abv повинен бути типу float"""
        product = Product.objects.create(name="Whisky", category="h", abv=43.0)
        self.assertIsInstance(product.abv, float)

    def test_create_product_and_str(self):
        product = Product.objects.create(name="Gin", description="Distilled spirit", category="h", abv=40.0, volume="0.7L", is_kosher=True, is_limited=False)
        self.assertEqual(product.name, "Gin")
        self.assertEqual(product.description, "Distilled spirit")
        self.assertEqual(product.category, "h")
        self.assertEqual(product.abv, 40.0)
        self.assertEqual(product.volume, "0.7L")
        self.assertTrue(product.is_kosher)
        self.assertFalse(product.is_limited)
        self.assertEqual(str(product), "Gin")

# ingredient tests

    def test_ingredient_name_length(self):
        """Довжина назви інгредієнта"""
        name = "VeryLongIngredientName"
        ingredient = Ingredient.objects.create(name=name)
        self.assertEqual(len(ingredient.name), len(name))

    def test_duplicate_ingredient(self):
        """Можна створити два інгредієнти з однаковим ім'ям"""
        i1 = Ingredient.objects.create(name="DuplicateIngredient")
        i2 = Ingredient.objects.create(name="DuplicateIngredient")
        self.assertNotEqual(i1.id, i2.id)

    def test_create_ingredient_and_str(self):
        ingredient = Ingredient.objects.create(name="Sugar")
        self.assertEqual(ingredient.name, "Sugar")
        self.assertEqual(str(ingredient), "Sugar")

# cocktail ingredient tests

    def test_cocktail_ingredient_empty_quantity(self):
        """Створення з порожнім quantity"""
        ingredient = Ingredient.objects.create(name="Bitters")
        cocktail = Cocktail.objects.create(name="Old Fashioned")
        ci = CocktailIngredient.objects.create(cocktail=cocktail, ingredient=ingredient, quantity="")
        self.assertEqual(ci.quantity, "")

    def test_multiple_ingredients_per_cocktail(self):
        """Додавання кількох інгредієнтів до одного коктейлю"""
        cocktail = Cocktail.objects.create(name="MultiIngredient")
        i1 = Ingredient.objects.create(name="A")
        i2 = Ingredient.objects.create(name="B")
        ci1 = CocktailIngredient.objects.create(cocktail=cocktail, ingredient=i1, quantity="10ml")
        ci2 = CocktailIngredient.objects.create(cocktail=cocktail, ingredient=i2, quantity="20ml")
        self.assertEqual(CocktailIngredient.objects.filter(cocktail=cocktail).count(), 2)

    def test_create_cocktail_ingredient_and_str(self):
        ingredient = Ingredient.objects.create(name="Lime Juice")
        cocktail = Cocktail.objects.create(name="Daiquiri")
        cocktail_ingredient = CocktailIngredient.objects.create(
            cocktail=cocktail,
            ingredient=ingredient,
            quantity="20ml"
        )
        self.assertEqual(cocktail_ingredient.cocktail, cocktail)
        self.assertEqual(cocktail_ingredient.ingredient, ingredient)
        self.assertEqual(cocktail_ingredient.quantity, "20ml")
        self.assertIn(str(ingredient), str(cocktail_ingredient))
        self.assertIn(str(cocktail), str(cocktail_ingredient))

# contact info tests

    def test_create_contact_info_and_str(self):
        contact = ContactInfo.objects.create(email="info@bar.com", phone="123456789")
        self.assertEqual(contact.email, "info@bar.com")
        self.assertEqual(contact.phone, "123456789")

    def test_contact_info_email_format(self):
        """Перевірка правильного збереження email"""
        email = "test@example.com"
        contact = ContactInfo.objects.create(email=email, phone="111")
        self.assertIn("@", contact.email)
        self.assertEqual(contact.email, email)

    def test_contact_info_blank_map_url(self):
        """map_embed_url може бути порожнім"""
        contact = ContactInfo.objects.create(email="a@b.com", phone="222", map_embed_url="")
        self.assertEqual(contact.map_embed_url, "")
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
