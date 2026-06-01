from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Product, Category

def products_view(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})

def product_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {'product': product})

def product_add_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        image = request.POST.get('image')
        category_id = request.POST.get('category')
        description = request.POST.get('description')
        product = Product.objects.create(
            name=name,
            price=price,
            image=image,
            category_id=category_id,
            description=description
        )
        return redirect(reverse('product_detail', args=[product.pk]))
    categories = Category.objects.all()
    return render(request, 'product_add.html', {'categories': categories})

def category_add_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        Category.objects.create(name=name, description=description)
        return redirect(reverse('products'))
    return render(request, 'category_add.html')
