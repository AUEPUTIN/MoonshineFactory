from django.db import models

class AboutPage(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='about_images/', blank=True, null=True)

    def __str__(self):
        return self.title

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('horilka', 'Горілка'),
        ('infusion', 'Настоянка'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    abv = models.DecimalField(max_digits=5, decimal_places=2)  # Alcohol by volume
    volume = models.CharField(max_length=50)  # e.g., '0.5L', '0.7L'
    image = models.ImageField(upload_to='product_images/')
    is_kosher = models.BooleanField(default=False)
    is_limited = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Cocktail(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='cocktail_images/')
    ingredients = models.ManyToManyField('Ingredient', through='CocktailIngredient')

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class CocktailIngredient(models.Model):
    cocktail = models.ForeignKey(Cocktail, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=100)  # e.g., '30 мл'

    def __str__(self):
        return f"{self.quantity} {self.ingredient.name} for {self.cocktail.name}"

class ContactInfo(models.Model):
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=50)
    email = models.EmailField()
    map_embed_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.address


