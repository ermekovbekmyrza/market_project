from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Product, Category
from .forms import ProductForm, SearchForm

def products_view(request):
    search_form = SearchForm(request.GET)
    products = Product.objects.filter(stock__gte=1).order_by('category__name', 'name')
    if search_form.is_valid():
        name = search_form.cleaned_data.get('name')
        if name:
            products = products.filter(name__icontains=name)
    return render(request, 'products.html', {
        'products': products
        'search_form': search_form
        })

def product_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {'product': product})

def product_add_view(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = Product.objects.create(
                name=form.cleaned_data['name'],
                price=form.cleaned_data['price'],
                image=form.cleaned_data['image'],
                category_id=form.cleaned_data['category'],
                description=form.cleaned_data['description'],
                stock=form.cleaned_data['stock']
            )
            return redirect(reverse('product_detail', args=[product.pk]))
    else:
        form = ProductForm()
    return render(request, 'product_add.html', {'form': form})

def product_edit_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product.name = form.cleaned_data['name']
            product.price = form.cleaned_data['price']
            product.image = form.cleaned_data['image']
            product.category_id = form.cleaned_data['category']
            product.description = form.cleaned_data['description']
            product.stock = form.cleaned_data['stock']
            product.save()
            return redirect(reverse('product_detail', args=[product.pk]))
    else:
        form = ProductForm(initial={
            'name': product.name,
            'price': product.price,
            'image': product.image,
            'category': product.category_id,
            'description': product.description,
            'stock': product.stock
        })
    return render(request, 'product_edit.html', {'form': form, 'product': product})

def product_delete_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect(reverse('products'))
    return render(request, 'product_confirm_delete.html', {'product': product})

def category_add_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        Category.objects.create(name=name, description=description)
        return redirect(reverse('products'))
    return render(request, 'category_add.html')

def category_products_view(request, pk):
    category = get_object_or_404(Category, pk=pk)
    search_form = SearchForm(request.GET)
    products = Product.objects.filter(
        category=category,
        stock__gte=1
    ).order_by('name')
    if search_form.is_valid():
        name = search_form.cleaned_data.get('name')
        if name:
            products = products.filter(name__icontains=name)
    return render(request, 'category_products.html', {
        'category': category,
        'products': products,
        'search_form': search_form
    })
