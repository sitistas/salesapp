from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from core.views import dashboard_view, SaleListView # Εδώ το νέο import

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', dashboard_view, name='dashboard'), # Η αρχική σελίδα
    path('sales/', SaleListView.as_view(), name='sale-list'),
]