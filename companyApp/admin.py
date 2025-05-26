from django.contrib import admin
from .models import Employee, Company

# Register your models here.

class EmployeeAdmin(admin.ModelAdmin):
  list_display = ('name', 'company','job_title')
admin.site.register(Employee, EmployeeAdmin)

class CompanyAdmin(admin.ModelAdmin):
  list_display = ('email', 'company_name')
admin.site.register(Company, CompanyAdmin)