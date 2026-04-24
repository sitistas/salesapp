from django.contrib import admin
from .models import User, Category, Product, Store, ActionType, Sale, Promotion, Competition, Announcement

# Καταγράφουμε όλα τα μοντέλα στο admin panel
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Store)
admin.site.register(ActionType)
admin.site.register(Sale)
admin.site.register(Promotion)
admin.site.register(Competition)
admin.site.register(Announcement)