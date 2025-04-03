from django.contrib import admin

from .models import Products, Invoice, Customer, InvoiceList, PurchaseList

admin.site.register(Products)
admin.site.register(Invoice)
admin.site.register(InvoiceList)
admin.site.register(Customer)
admin.site.register(PurchaseList)

