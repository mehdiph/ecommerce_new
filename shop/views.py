from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm

# Create your views here.
def product_list(request, category_slug=None):
    products = Product.objects.all()
    categories = Category.objects.all()
    print(categories[0].products.all())
    category = None

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category)

    return render(request, 'shop/index.html', {'products': products, 'categories': categories, 'category': category})

def product_detail(request, id, slug):
    product = get_object_or_404(
    Product, id=id, slug=slug, available=True
    )
    form = CartAddProductForm()
    return render(request, 'shop/detail.html', {'product': product, 'form': form})


