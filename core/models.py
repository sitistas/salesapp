from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class SoftDeleteModel(models.Model):
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True  # Αυτό σημαίνει ότι δεν θα φτιαχτεί πίνακας στη βάση γι' αυτό

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()

# --- 1. Custom User Model ---
class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin/Superadmin'),
        ('promoter', 'Promoter'),
        ('client', 'Client'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='promoter')

    def delete(self, *args, **kwargs):
        """Soft delete: Απενεργοποίηση αντί για οριστική διαγραφή"""
        self.is_active = False
        self.save()
        # Δεν καλούμε το super().delete() για να μην σβηστεί η εγγραφή

# --- 2. Soft Delete Logic (Base Model) ---
class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    class Meta:
        abstract = True

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()

# --- 3. Business Logic Models ---

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    sku = models.CharField(max_length=50, unique=True) # Κωδικός
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return f"{self.sku} - {self.name}"

class Store(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=300, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)  # Soft delete flag

    def delete(self, *args, **kwargs):
        # Αντί για κανονική διαγραφή, κάνουμε soft delete
        self.is_active = False
        self.save()
        # Δεν καλούμε το super().delete(), οπότε η εγγραφή μένει στη βάση!

    def __str__(self):
        return self.name
    
class ActionType(BaseModel):
    name = models.CharField(max_length=100)
    def __str__(self): return self.name

# --- 4. Transactional Models (Sales, Promotions, Competition) ---

class Sale(BaseModel):
    date = models.DateField(auto_now_add=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    salesperson = models.ForeignKey(User, on_delete=models.CASCADE)

class Promotion(BaseModel):
    date = models.DateField()
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    action_type = models.ForeignKey(ActionType, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    salesperson = models.ForeignKey(User, on_delete=models.CASCADE)

class Competition(BaseModel):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    comments = models.TextField()
    salesperson = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        verbose_name_plural = "Competition"

class Announcement(BaseModel):
    title = models.CharField(max_length=200)
    body = models.TextField()
    is_active = models.BooleanField(default=True)
