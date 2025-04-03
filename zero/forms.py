from django import forms
from .models import Invoice, Products, Customer, InvoiceList, PurchaseList

class CustomerForm(forms.ModelForm):
	class Meta:
		model = Customer
		fields = ['customername', 'mobileno']

class InvoiceForm(forms.ModelForm):
	class Meta:
		model = Invoice
		fields = ['mobile']
	

class ProductsForm(forms.ModelForm):
	class Meta:
		model = Products
		fields = ['productname', 'price','purchaseprice','inwardqnty']

class InvoiceListForm(forms.ModelForm):
	class Meta:
		model = InvoiceList
		fields = ['product','quantity']

class PurchaseListForm(forms.ModelForm):
	class Meta:
		model = PurchaseList
		fields = ['product','purchaseprice','purchaseqnty']
	

				