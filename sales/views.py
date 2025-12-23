from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Sale, SaleItem
from .forms import SaleForm, SaleItemFormSet
from inventory.models import Product, StockTransaction

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

class SaleListView(LoginRequiredMixin, ListView):
    model = Sale
    template_name = 'sales/sale_list.html'
    context_object_name = 'sales'
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        date_query = self.request.GET.get('date')
        if date_query:
            queryset = queryset.filter(created_at__date=date_query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date_query'] = self.request.GET.get('date', '')
        return context

class SaleDetailView(LoginRequiredMixin, DetailView):
    model = Sale
    template_name = 'sales/sale_detail.html'
    context_object_name = 'sale'

class SaleCreateView(LoginRequiredMixin, CreateView):
    model = Sale
    form_class = SaleForm
    template_name = 'sales/sale_form.html'
    success_url = reverse_lazy('sales:sale_list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['items'] = SaleItemFormSet(self.request.POST)
        else:
            data['items'] = SaleItemFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        items = context['items']
        
        if items.is_valid():
            with transaction.atomic():
                self.object = form.save()
                items.instance = self.object
                saved_items = items.save()
                
                # Calculate total amount and update stock
                total_amount = 0
                for item in saved_items:
                    total_amount += item.total_price
                    
                    # Update stock
                    product = item.product
                    # Stock validation is handled in formset clean method
                    
                    product.stock_quantity -= item.quantity
                    product.save()
                    
                    # Create StockTransaction
                    StockTransaction.objects.create(
                        product=product,
                        transaction_type='OUT',
                        quantity=item.quantity,
                        note=f"Sale #{self.object.id}"
                    )

                self.object.total_amount = total_amount
                self.object.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))
