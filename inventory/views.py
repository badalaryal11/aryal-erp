from django.shortcuts import render, redirect
from django.http import HttpResponse
import csv
import openpyxl
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from django.contrib import messages
from .models import Product, Category
from .forms import ProductForm

from django.db.models import Q

from django.contrib.auth.decorators import login_required, permission_required

@login_required
@permission_required('inventory.view_product', raise_exception=True)
def product_list(request):
    query = request.GET.get('q', '')
    products = Product.objects.all().select_related('category')
    
    if query:
        products = products.filter(
            Q(name__icontains=query) | 
            Q(code__icontains=query)
        )
    
    return render(request, 'inventory/product_list.html', {'products': products, 'query': query})

@login_required
@permission_required('inventory.add_product', raise_exception=True)
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

@login_required
@permission_required('inventory.view_product', raise_exception=True)
def export_products(request):
    format_type = request.GET.get('format', 'csv')
    products = Product.objects.all().select_related('category')

    if format_type == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="inventory.csv"'
        writer = csv.writer(response)
        writer.writerow(['Name', 'Code', 'Category', 'Packaging', 'Price', 'Stock', 'Cost Price'])
        for product in products:
            writer.writerow([product.name, product.code, product.category.name if product.category else '-', product.packaging or '-', product.price, product.stock_quantity, product.cost_price])
        return response

    elif format_type == 'excel':
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="inventory.xlsx"'
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Inventory"
        headers = ['Name', 'Code', 'Category', 'Packaging', 'Price', 'Stock', 'Cost Price']
        ws.append(headers)
        for product in products:
            ws.append([product.name, product.code, product.category.name if product.category else '-', product.packaging or '-', product.price, product.stock_quantity, product.cost_price])
        wb.save(response)
        return response

    elif format_type == 'pdf':
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="inventory.pdf"'
        
        doc = SimpleDocTemplate(response, pagesize=letter)
        elements = []
        
        data = [['Name', 'Code', 'Category', 'Packaging', 'Price', 'Stock', 'Cost Price']]
        for product in products:
            data.append([
                product.name,
                product.code,
                product.category.name if product.category else '-',
                product.packaging or '-',
                str(product.price),
                str(product.stock_quantity),
                str(product.cost_price)
            ])
            
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(table)
        doc.build(elements)
        return response

    return redirect('product_list')
