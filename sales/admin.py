from django.contrib import admin
from .models import Sale, SaleItem

class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 1

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'total_amount', 'payment_method')
    list_filter = ('payment_method', 'created_at')
    inlines = [SaleItemInline]
