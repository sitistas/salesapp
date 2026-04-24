from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .models import Sale, Promotion, Announcement

@login_required
def dashboard_view(request):
    user = request.user
    
    # Αρχικά Querysets
    sales_qs = Sale.objects.all()
    promos_qs = Promotion.objects.all()

    # Αν είναι Promoter, βλέπει ΜΟΝΟ τα δικά του (spec requirement!)
    if user.role == 'promoter':
        sales_qs = sales_qs.filter(salesperson=user)
        promos_qs = promos_qs.filter(salesperson=user)

    # Υπολογισμός Συνόλων (Sum)
    total_sales = sales_qs.aggregate(Sum('quantity'))['quantity__sum'] or 0
    total_promos = promos_qs.aggregate(Sum('quantity'))['quantity__sum'] or 0

    # Τελευταίες 10 πωλήσεις
    recent_sales = sales_qs.order_by('-date')[:10]

    context = {
        'total_sales': total_sales,
        'total_promos': total_promos,
        'recent_sales': recent_sales,
    }
    
    return render(request, 'dashboard.html', context)