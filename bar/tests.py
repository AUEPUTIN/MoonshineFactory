import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE","djangoProject1.settings")
django.setup()
from django.core.exceptions import ValidationError
from django.test import TestCase
from bar.models import Cocktail, Ingredient, AboutPage, Product, CocktailIngredient, ContactInfo

# ------------------ Model classes tests ------------------

class ModelsTests(TestCase):

# cocktail tests

    def test_cocktail_without_description(self):
        cocktail = Cocktail.objects.create(name="NoDescCocktail")
        self.assertEqual(cocktail.description, "")

    def test_cocktail_duplicate_name(self):
        c1 = Cocktail.objects.create(name="DuplicateName")
        c2 = Cocktail.objects.create(name="DuplicateName")
        self.assertNotEqual(c1.id, c2.id)

    def test_create_cocktail(self):
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
        cocktail = Cocktail.objects.create(
            name="Margarita",
            description="Shake with ice and strain into a glass."
        )
        ingredients = [Ingredient.objects.create(name=name) for name in ["Tequila", "Lime", "Triple Sec"]]
        cocktail.ingredients.set(ingredients)
        self.assertEqual(str(cocktail), "Margarita")

    def test_name_required(self):
        cocktail = Cocktail(description="Mix vodka and tonic.")
        with self.assertRaises(ValidationError):
            cocktail.full_clean()

    def test_empty_ingredients_and_description(self):
        cocktail = Cocktail.objects.create(
            name="Simple Cocktail",
            description=""
        )
        self.assertEqual(cocktail.name, "Simple Cocktail")
        self.assertEqual(cocktail.ingredients.count(), 0)
        self.assertEqual(cocktail.description, "")

    def test_minimal_cocktail(self):
        cocktail = Cocktail.objects.create(name="Basic Cocktail")
        self.assertEqual(cocktail.name, "Basic Cocktail")
        self.assertEqual(cocktail.ingredients.count(), 0)
        self.assertEqual(cocktail.description, "")

# about page tests

    def test_about_page_with_empty_image(self):
        about = AboutPage.objects.create(title="No Image", content="No image here")
        self.assertFalse(about.image)

    def test_about_page_content_length(self):
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
        product = Product.objects.create(name="Vodka", category="h", abv=37.5, is_kosher=False, is_limited=True)
        self.assertFalse(product.is_kosher)
        self.assertTrue(product.is_limited)

    def test_product_abv_type(self):
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
        name = "VeryLongIngredientName"
        ingredient = Ingredient.objects.create(name=name)
        self.assertEqual(len(ingredient.name), len(name))

    def test_duplicate_ingredient(self):
        i1 = Ingredient.objects.create(name="DuplicateIngredient")
        i2 = Ingredient.objects.create(name="DuplicateIngredient")
        self.assertNotEqual(i1.id, i2.id)

    def test_create_ingredient_and_str(self):
        ingredient = Ingredient.objects.create(name="Sugar")
        self.assertEqual(ingredient.name, "Sugar")
        self.assertEqual(str(ingredient), "Sugar")

# cocktail ingredient tests

    def test_cocktail_ingredient_empty_quantity(self):
        ingredient = Ingredient.objects.create(name="Bitters")
        cocktail = Cocktail.objects.create(name="Old Fashioned")
        ci = CocktailIngredient.objects.create(cocktail=cocktail, ingredient=ingredient, quantity="")
        self.assertEqual(ci.quantity, "")

    def test_multiple_ingredients_per_cocktail(self):
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
        email = "test@example.com"
        contact = ContactInfo.objects.create(email=email, phone="111")
        self.assertIn("@", contact.email)
        self.assertEqual(contact.email, email)

    def test_contact_info_blank_map_url(self):
        contact = ContactInfo.objects.create(email="a@b.com", phone="222", map_embed_url="")
        self.assertEqual(contact.map_embed_url, "")