from django.db import models
from django.urls import reverse
from shop.settings import AUTH_USER_MODEL
from django.utils import timezone

# Create your models here.
"""
Product
- Nom
- Prix
- stock
- Description
- Image

"""

class Product(models.Model):
	name = models.CharField(max_length=128) #text court
	slug = models.SlugField(max_length=128)
	price = models.FloatField(default=0.0)
	stock = models.IntegerField(default=0)
	description = models.TextField(blank=True) # peut etre vide
	thumbnail = models.ImageField(upload_to="products", blank=True, null=True)

	def __str__(self):
		return f"{self.name} ({self.stock})"
	
	#btn voir sur le site ds bd
	def get_absolute_url(self): 
		return reverse("product", kwargs={"slug": self.slug})

#Article (Order)
"""
-User
-Product
-Quantity
- oder or no
"""
class Order(models.Model):
	#user can has many products 
	user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity = models.IntegerField(default=1)
	ordered = models.BooleanField(default=False)
	ordered_date = models.DateTimeField(blank=True, null=True)

	def __str__(self):
		return f"{self.product.name} ({self.quantity})"

#Panier(Cart)
"""
-uer
-Product
-order or no
-date of order
"""	

class Cart(models.Model):
	#user can has 1 cart in same time
	user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)
	orders = models.ManyToManyField(Order)

	def __str__(self):
		return self.user.username
	
	def delete(self, *args, **kwargs):
		for order in self.orders.all():
			order.ordered = True
			order.ordered_date = timezone.now()
			order.save()
		self.orders.clear()
		super().delete(*args, **kwargs)