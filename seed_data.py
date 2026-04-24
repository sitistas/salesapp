import os
import django
import random
from datetime import datetime, timedelta

# Ρύθμιση του Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import User, Store, Category, Product, Sale, ActionType

def seed_data():
    print("Ξεκινάω τη μαζική καταχώρηση...")

    # 1. Δημιουργία Καταστημάτων
    stores_names = ["Πλαίσιο Συντάγματος", "Public Τσιμισκή", "Κωτσόβολος Mall", "MediaMarkt Ρέντη"]
    stores = [Store.objects.get_or_create(name=name)[0] for name in stores_names]

    # 2. Δημιουργία Κατηγοριών & Προϊόντων
    cat_tech, _ = Category.objects.get_or_create(name="Τεχνολογία")
    products_data = [
        ("SKU001", "Smartphone X1", cat_tech),
        ("SKU002", "Laptop Pro 15", cat_tech),
        ("SKU003", "Wireless Buds", cat_tech),
    ]
    products = [Product.objects.get_or_create(code=c, name=n, category=cat)[0] for c, n, cat in products_data]

    # 3. Χρήστες (Βεβαιώσου ότι έχεις έναν promoter)
    promoter, created = User.objects.get_or_create(username="promoter1")
    if created:
        promoter.set_password("pass123")
        promoter.role = "promoter"
        promoter.first_name = "Γιώργος"
        promoter.last_name = "Παπαδόπουλος"
        promoter.save()

    # 4. Δημιουργία Πωλήσεων (τυχαίες ημερομηνίες τελευταίων 30 ημερών)
    for _ in range(30):
        random_days = random.randint(0, 30)
        random_date = datetime.now().date() - timedelta(days=random_days)
        
        Sale.objects.create(
            date=random_date,
            store=random.choice(stores),
            product=random.choice(products),
            quantity=random.randint(1, 10),
            salesperson=promoter
        )

    print(f"Επιτυχία! Δημιουργήθηκαν {Sale.objects.count()} πωλήσεις.")

if __name__ == "__main__":
    seed_data()