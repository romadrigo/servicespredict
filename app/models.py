from asyncio.windows_events import NULL
from email.policy import default
from enum import unique
from errno import EDQUOT
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser, BaseUserManager
# Create your models here.

class Company(models.Model):
    number = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)

# class UserCompany(models.Model):
#     user = models.ForeignKey(User, editable=True, on_delete=models.CASCADE)
#     company = models.ForeignKey(Company, editable=True, on_delete=models.CASCADE)

class CustomUserManager(BaseUserManager):
    def create_user(self, first_name, username, company, role, email, password = None):
        if not email:
            raise ValueError('El usuario debe tener un correo electrónico')
        
        user = self.model(
            first_name= first_name,
            username = username,
            company = company,
            role = role, 
            email = self.normalize_email(email)
        )

        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, first_name, username, company, email, password = None):
        user = self.create_user(  
            first_name= first_name,
            username = username, 
            company = company, 
            role = "SuperAdmin", 
            email = email, 
            password = password)
        return user
class CustomUser(AbstractUser):
    # username = models.CharField(max_length=50, default = "")
    # email = models.EmailField(unique = True, max_length=100)
    company = models.ForeignKey(Company, editable=True, on_delete=models.CASCADE)
    role =  models.CharField(max_length=20, default= None)
    token_reset_password =  models.CharField(max_length=20, default= None)
    objects = CustomUserManager()
    
    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['email']

    def __str__(self):
        return f'{self.username}'
    
    def has_perm(self, perm, obj = None ):
        return True
    
    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.role == 'SuperAdmin'

class FinancialEntity(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(CustomUser, editable=False, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    # logo = models.CharField(max_length=100)

class Phone(models.Model):
    number = models.CharField(max_length=9)
    financial_entity = models.ForeignKey(FinancialEntity, editable=True, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, editable=False, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)

class HistoryCall(models.Model):
    name = models.CharField(max_length=50)
    name_upload = models.CharField(max_length=50, default="")
    user = models.ForeignKey(CustomUser, editable=False, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)


class HistoryCallDetail(models.Model):
    history_call = models.ForeignKey(HistoryCall, editable=False, on_delete=models.CASCADE)
    financial_entity = models.ForeignKey(FinancialEntity, editable=True, on_delete=models.CASCADE)
    phone = models.ForeignKey(Phone, editable=True, on_delete=models.CASCADE)
    hour = models.CharField(max_length=10)
    state = models.CharField(max_length=50)
    call_duration = models.CharField(max_length=10, default ="")
    call_date = models.CharField(max_length=10, default ="")
    # user = models.ForeignKey(User, editable=False, on_delete=models.CASCADE)
    # created_at = models.DateTimeField(auto_now=False, auto_now_add=True)

class CategoryHour(models.Model):
    idd = models.CharField(max_length=2)
    name = models.CharField(max_length=50)
    first = models.CharField(max_length=10)
    second = models.CharField(max_length=10)

class Report(models.Model):
    phone = models.ForeignKey(Phone, editable=True, on_delete=models.CASCADE)
    category_range = models.ForeignKey(CategoryHour, editable=True,on_delete=models.CASCADE)
    day = models.CharField(max_length=1, default= None)
    prediction_result = models.CharField(max_length=10, default= None)
    predicted_at = models.DateTimeField(auto_now=False, auto_now_add=False)
    filter_hours = models.CharField(max_length=250, default="[]")
    user = models.ForeignKey(CustomUser, editable=False, default= None, on_delete=models.CASCADE)


    