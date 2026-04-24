from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# --- 1. Custom User Model ---
class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin/Superadmin'),
        ('promoter', 'Promoter'),
        ('client', 'Client'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='promoter')

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

class Category(BaseModel):
    name = models.CharField(max_length=100)
    def __str__(self): return self.name

class Product(BaseModel):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    def __str__(self): return f"{self.code} - {self.name}"

class Store(BaseModel):
    name = models.CharField(max_length=200)
    def __str__(self): return self.name

class ActionType(BaseModel):
    name = models.CharField(max_length=100)
    def __str__(self): return self.name

# --- 4. Transactional Models (Sales, Promotions, Competition) ---

class Sale(BaseModel):
    date = models.DateField()
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
    date = models.DateField()
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    comment = models.TextField()
    salesperson = models.ForeignKey(User, on_delete=models.CASCADE)

class Announcement(BaseModel):
    title = models.CharField(max_length=200)
    body = models.TextField()
    is_active = models.BooleanField(default=True)