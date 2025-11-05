from django.contrib import admin
from .models import Stock, Portfolio, Transaction

admin.site.register(Stock)
admin.site.register(Portfolio)
admin.site.register(Transaction)

# Register your models here.
