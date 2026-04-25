from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from core.views import *
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
    path('competition/export/', export_competition_excel, name='competition-export'),
    path('sales-status/', SalesStatusView.as_view(), name='sales-status'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/category/add/', add_category, name='add-category'),
    path('stores/', StoreListView.as_view(), name='store-list'),
    path('stores/add/', StoreCreateView.as_view(), name='store-create'),
    path('stores/<int:pk>/edit/', StoreUpdateView.as_view(), name='store-update'),
    path('stores/<int:pk>/delete/', StoreDeleteView.as_view(), name='store-delete'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/add/', UserCreateView.as_view(), name='user-create'),
    path('users/<int:pk>/edit/', UserUpdateView.as_view(), name='user-update'),
    path('users/<int:pk>/delete/', UserDeleteView.as_view(), name='user-delete'),
]