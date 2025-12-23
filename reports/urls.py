from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.ReportDashboardView.as_view(), name='dashboard'),
    path('download/top-selling/', views.download_top_selling_csv, name='download_top_selling'),
    path('download/low-stock/', views.download_low_stock_csv, name='download_low_stock'),
    path('download/recent-sales/', views.download_recent_sales_csv, name='download_recent_sales'),
    path('download/daily-sales/', views.download_daily_sales_csv, name='download_daily_sales'),
    path('download/monthly-sales/', views.download_monthly_sales_csv, name='download_monthly_sales'),
    path('download/yearly-sales/', views.download_yearly_sales_csv, name='download_yearly_sales'),
]
