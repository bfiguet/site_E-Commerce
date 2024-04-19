from django.shortcuts import render, get_object_or_404, redirect
from store.models import Product, Cart, Order
from django.http import HttpResponse
from django.urls import reverse

# Create your views here.
def index(request):
	products = Product.objects.all()
	#Product.objects.all(filter(stock)) # filter que les produits en stocks
	return render(request, 'store/index.html', context={"products": products})

def product_detail(request, slug):
	product = get_object_or_404(Product, slug=slug)
	return render(request, 'store/detail.html', context={"product": product})

def add_to_cart(request, slug):
	#user.add_to_cart(poduct) -> peu-etre fait ds models
	user = request.user
	product = get_object_or_404(Product, slug=slug)
	cart, _ = Cart.objects.get_or_create(user=user)
	# _ convention we don't use second var returned by get_or_created
	order, created = Order.objects.get_or_create(user=user, ordered=False, product=product)
	# if product is already in cart update nb of product else add this product
 	#created is bool

	if created:
		cart.orders.add(order)
		cart.save()
	else:
		order.quantity += 1
		order.save()

	return redirect(reverse("product", kwargs={"slug":slug}))

def cart(request):
	cart = get_object_or_404(Cart, user=request.user)
	return render(request, 'store/cart.html', context={"orders": cart.orders.all()})

def delete_cart(request):
	# := walrus before cart = request.user.cart if cart: 
	if cart := request.user.cart:
		cart.delete() 
	return redirect('index') 