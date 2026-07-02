from django.db import models
from products.models import Product, TimeStampModel
from accounts.models import CustomUser

# Create your models here.

class Cart(TimeStampModel):
    session_key = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.session_key
    
class CartItem(TimeStampModel):
    # user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, null=True)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, null=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)

    def sub_total(self):
        return self.product.discount_price * self.quantity
    
    def __str__(self):
        return f"CartItem {self.product.name}"
    
    

