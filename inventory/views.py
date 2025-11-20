from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Product, Category
from .forms import ProductForm

from django.db.models import Q

def product_list(request):
    query = request.GET.get('q', '')
    products = Product.objects.all().select_related('category')
    
    if query:
        products = products.filter(
            Q(name__icontains=query) | 
            Q(code__icontains=query)
        )
    
    return render(request, 'inventory/product_list.html', {'products': products, 'query': query})

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product created successfully!')
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'inventory/product_form.html', {'form': form})
