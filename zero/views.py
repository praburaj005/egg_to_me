from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError
from .models import Products, Invoice, Customer, InvoiceList, PurchaseList
from .forms import InvoiceForm, ProductsForm, CustomerForm, InvoiceListForm, PurchaseListForm
import csv
from django.http import HttpResponse
from django.db import transaction
from django.contrib.auth.decorators import login_required


def login(request):
	if request.user.is_authenticated:
		return render(request, 'home.html')
	else:
		return render(request, 'login.html')
def logout(request):
	logout(request)
	return redirect('home')

def home(request):
	
	products = Products.objects.all()
	product_dic = {product.productid:{'product_price':product.price,'product_name':product.productname,'product_date':product.purchasedate} for product in products}
	context = {'products': Products.objects.all(),'product_dic':product_dic}

	return render(request, 'home.html', context)

def createinvoiceid(request):
	customers = Customer.objects.all()
	if request.method == 'POST':
		form = InvoiceForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('createinvoice')
	
	else:
		form = InvoiceForm()
	context = {'form': form,'customers':customers}

	return render(request, 'createinvoiceid.html', context)	

def createinvoice(request):
	products = Products.objects.all()
	invoice_id = Invoice.objects.latest('invoiceid')
	if request.method == 'POST':
		form = InvoiceListForm(request.POST)
		if form.is_valid():
			try:	
				form.instance.invoiceid = invoice_id
				form.save()
				return redirect('createinvoice')
			except ValidationError as e:
				error_message = str(e)
				return render(request, 'createinvoice.html', {'form': form, 'error_message': error_message})
	else:
		form = InvoiceListForm()

	context = {'form': form, 'invoice_id':invoice_id}

	return render(request, 'createinvoice.html', context)

def print(request):
	latest_invoice = Invoice.objects.latest('invoiceid')
	invoice_items = InvoiceList.objects.filter(invoiceid=latest_invoice)
	latest_mobile = latest_invoice.mobile
	customer_name = Customer.objects.get(mobileno=latest_mobile)
	latest_customername = customer_name.customername
	context = {'latest_invoice': latest_invoice,'invoice_items': invoice_items,'latest_mobile': latest_mobile,'latest_customername': latest_customername}
	return render(request, 'print.html', context)

@login_required
def addproduct(request):
	if request.method == 'POST':
		form = ProductsForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('home')
	else:
		form = ProductsForm()
	context = {'products': Products.objects.all(),'form': form,}

	return render(request, 'addproduct.html', context)

@login_required
def addpurchase(request):
	if request.method == 'POST':
		form = PurchaseListForm(request.POST)
		if form.is_valid():
			with transaction.atomic():
				purchase = form.save()
				product = purchase.product
				product.inwardqnty += purchase.purchaseqnty
				product.purchaseprice = purchase.purchaseprice
				product.save()
				return redirect('home')
	else:
		form = PurchaseListForm()
	context = {'form': form,}

	return render(request, 'addpurchase.html', context)

@login_required
def addcustomer(request):
	if request.method == 'POST':
		form = CustomerForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('home')
	else:
		form = CustomerForm()
	context = {'form': form,}

	return render(request, 'addcustomer.html', context)

@login_required
def invoice(request):
	invoices = Invoice.objects.all()
	customers = Customer.objects.all()
	total_amount = sum(invoice.total for invoice in invoices)
	customer_map = {customer.mobileno: customer.customername for customer in customers}
	context = {'invoices':invoices,'customer_map':customer_map,'total_amount':total_amount, 'customers':customers}
	return render(request, 'invoice.html', context)

def purchasedetails(request):
	purchases = PurchaseList.objects.all()
	context = {'purchases':purchases,}
	return render(request, 'purchasedetails.html', context)

@login_required
def updateproduct(request, productid):
	
	product = get_object_or_404(Products, productid = productid)
	
	if request.method == 'POST':
		form = ProductsForm(request.POST, instance = product)
		if form.is_valid():
			form.save()
			return redirect('home')
	else:
		form = ProductsForm(instance = product)
	context = {'products': Products.objects.all(),'form': form,}

	return render(request, 'updateproduct.html', context)

def updateinvoice(request, invoiceid):
	
	product = get_object_or_404(Invoice, invoiceid = invoiceid)
	
	if request.method == 'POST':
		form = InvoiceForm(request.POST, instance = product)
		if form.is_valid():
			form.save()
			return redirect('invoice')
	else:
		form = InvoiceForm(instance = product)
	context = {'products': Invoice.objects.all(),'form': form,}

	return render(request, 'updateinvoice.html', context)

def customer(request):
	customers = Customer.objects.all()
	context = {'customers': customers,}
	return render(request, 'customer.html', context)

def mobilefilter(request, mobileno):
	mobile = get_object_or_404(Customer, mobileno=mobileno)	
	invoices = Invoice.objects.filter(mobile = mobile).all()
	total_amount = sum(invoice.total for invoice in invoices)		
	context = {'invoices': invoices,'total_amount':total_amount}
	return render(request, 'invoice.html', context)

def download(request):
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename=invoice.csv'
	writer = csv.writer(response)
	writer.writerow(['Invoice ID', 'Product', 'Quantity', 'Total'])

	for obj in InvoiceList.objects.all():
		writer.writerow([obj.invoiceid, obj.product, obj.quantity, obj.total])
	return response


	


	


