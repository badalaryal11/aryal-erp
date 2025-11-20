from django.contrib import admin
from .models import Customer, SaleOrder, SaleItem, Invoice

class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 1

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email')
    search_fields = ('name', 'phone')

@admin.register(SaleOrder)
class SaleOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'date', 'total_amount', 'status')
    list_filter = ('status', 'date')
    inlines = [SaleItemInline]

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('order', 'created_at')
