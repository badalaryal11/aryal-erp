from django.urls import path
from . import views

app_name = 'sales'

urlpatterns = [
    path('', views.SaleListView.as_view(), name='sale_list'),
    path('create/', views.SaleCreateView.as_view(), name='sale_create'),
    path('<int:pk>/', views.SaleDetailView.as_view(), name='sale_detail'),
    path('<int:pk>/invoice/', views.SaleInvoiceView.as_view(), name='sale_invoice'),
]
