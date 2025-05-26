from django.db import models
from . manager import *
from django.contrib.auth.models import AbstractUser , Group , Permission
from django.utils import timezone

# Create your models here.


class Company(AbstractUser):
 
    username = None
    email = models.EmailField(unique=True,null=True,blank=True)
    is_email_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    company_name=models.CharField(max_length=20,null=True,blank=True)
    address=models.CharField(max_length=50,null=True,blank=True)
    otp = models.IntegerField(null=True, blank=True)
   
    USERNAME_FIELD = 'email'
 
    REQUIRED_FIELDS = []
    groups = models.ManyToManyField(Group, related_name="company_groups")  # ✅ Fix
    user_permissions = models.ManyToManyField(Permission, related_name="company_permissions")
 
    objects = UserManager()
   
    def __str__(self):
        return self.email 
    


class Employee(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    image = models.ImageField(upload_to='images/')
    job_title = models.CharField(max_length=50)
    salary = models.IntegerField()
    company = models.ForeignKey(Company, on_delete= models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.name


