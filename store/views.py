from django.shortcuts import render, get_object_or_404
from store.models import Product
from django.http import HttpResponse

# Create your views here.
def index(request):
	products = Product.objects.all()
	#Product.objects.all(filter(stock)) # filter que les produits en stocks
	return render(request, 'store/index.html', context={"products": products})

def product_detail(request, slug):
	product = get_object_or_404(Product, slug=slug)
	return render(request, 'store/detail.html', context={"product": product})