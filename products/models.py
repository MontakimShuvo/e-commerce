from django.db import models
from django.utils.text import slugify
from accounts.models import CustomUser
from django.db.models import Avg, Count

# Create your models here.

class TimeStampModel(models.Model):

    """
    An abstract base class model that provides self-managed 'created_at' and 'updated_at' fields.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Category(TimeStampModel):
    category_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    category_image = models.ImageField(upload_to='category_images')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.category_name)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.category_name

class Product(TimeStampModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    unit = models.CharField(max_length=100, blank=True, null=True)
    rating = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, null=True, blank=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def discount_price(self):
        return self.price *(1 - (self.discount_percentage / 100))
    
    @property
    def savings(self):
        return self.price - self.discount_price
    
    def get_discounted_price(self):
        if self.discount_price:
            return self.discount_price
        return self.price
    
    class Meta:
        ordering = ('-created_at',)
    
    def __str__(self) -> str:
        return self.name
    

class Review(TimeStampModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user')
    rating = models.FloatField()
    comment = models.TextField(blank=True)

    class Meta:
        unique_together = ('product', 'user')  # Ensure a user can only review a product once

    def __str__(self) -> str:
        return f"Review by {self.user.username} for {self.product.name}"
        

    
