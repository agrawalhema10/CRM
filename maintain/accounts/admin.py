from django.contrib import admin

# Register your models h
from .models import *
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Tag)
