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
from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
from .models import Sale
from .models import Competition

class CompetitionListView(LoginRequiredMixin, ListView):
    model = Competition
    template_name = 'competition/competition_list.html'
    context_object_name = 'entries'
    
    def get_queryset(self):
        # Οι Promoters βλέπουν μόνο τα δικά τους
        if self.request.user.role == 'promoter':
            return Competition.objects.filter(salesperson=self.request.user).select_related('store')
        return Competition.objects.all().select_related('store', 'salesperson')

class CompetitionCreateView(LoginRequiredMixin, CreateView):
    model = Competition
    fields = ['store', 'comments']
    template_name = 'competition/competition_form.html'
    success_url = reverse_lazy('competition-list')

    def form_valid(self, form):
        form.instance.salesperson = self.request.user
        return super().form_valid(form)
    

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
    paginate_by = 50

    def get_queryset(self):
        queryset = Sale.objects.all().select_related('product', 'store', 'salesperson')
        
        # 1. Φιλτράρισμα βάσει ρόλου (το κρατάμε!)
        if self.request.user.role == 'promoter':
            queryset = queryset.filter(salesperson=self.request.user)

        # 2. Αναζήτηση (Search)
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(store__name__icontains=q) | queryset.filter(product__name__icontains=q)

        # 3. Φιλτράρισμα Ημερομηνίας
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        if start_date and end_date:
            queryset = queryset.filter(date__range=[start_date, end_date])

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
    
def export_sales_excel(request):
    # Δημιουργία του response με το σωστό header για Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="Sales_Report.xlsx"'

    # Δημιουργία αρχείου
    wb = Workbook()
    ws = wb.active
    ws.title = "Πωλήσεις"

    # Ορισμός κεφαλίδων
    headers = ['Ημερομηνία', 'Κατάστημα', 'Προϊόν', 'Ποσότητα', 'Promoter']
    ws.append(headers)

    # Μορφοποίηση κεφαλίδων (Bold & Center)
    header_font = Font(bold=True)
    for cell in ws[1]:
        cell.font = header_font
        cell.alignment = Alignment(horizontal='center')

    # Φιλτράρισμα δεδομένων (Role-based)
    sales = Sale.objects.all().select_related('store', 'product', 'salesperson').order_by('-date')
    
    if request.user.role == 'promoter':
        sales = sales.filter(salesperson=request.user)

    # Προσθήκη δεδομένων
    for sale in sales:
        ws.append([
            sale.date.strftime("%d/%m/%Y"),
            sale.store.name,
            sale.product.name,
            sale.quantity,
            sale.salesperson.get_full_name() or sale.salesperson.username
        ])

    # Αυτόματη ρύθμιση πλάτους στηλών
    for col in ws.columns:
        max_length = 0
        column = col[0].column_letter
        for cell in col:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except: pass
        ws.column_dimensions[column].width = max_length + 2

    wb.save(response)
    return response