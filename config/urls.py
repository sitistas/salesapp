from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from core.views import dashboard_view, SaleListView, SaleCreateView,export_sales_excel,CompetitionListView, CompetitionCreateView # Εδώ το νέο import

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', dashboard_view, name='dashboard'), # Η αρχική σελίδα
    path('sales/', SaleListView.as_view(), name='sale-list'),
    path('sales/add/', SaleCreateView.as_view(), name='sale-create'), # Νέο path
    path('sales/export/', export_sales_excel, name='sale-export'),
    path('competition/', CompetitionListView.as_view(), name='competition-list'),
    path('competition/add/', CompetitionCreateView.as_view(), name='competition-create'),
]