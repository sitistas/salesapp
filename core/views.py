from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .models import Sale, Promotion, Announcement
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Sale
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import SaleForm

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

class SaleListView(LoginRequiredMixin, ListView):
    model = Sale
    template_name = 'sales/sale_list.html'
    context_object_name = 'sales'
    paginate_by = 50  # Spec requirement

    def get_queryset(self):
        queryset = super().get_queryset().select_related('product', 'store', 'salesperson')
        if self.request.user.role == 'promoter':
            queryset = queryset.filter(salesperson=self.request.user)
        return queryset.order_by('-date', '-created_at')
    
class SaleCreateView(LoginRequiredMixin, CreateView):
    model = Sale
    form_class = SaleForm
    template_name = 'sales/sale_form.html'
    success_url = reverse_lazy('sale-list')

    def form_valid(self, form):
        # Αυτόματη ανάθεση του συνδεδεμένου χρήστη ως salesperson
        form.instance.salesperson = self.request.user
        return super().form_valid(form)