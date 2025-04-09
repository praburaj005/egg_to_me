from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

class Customer(models.Model):
	mobile_validator = RegexValidator(r'^\d{10}$', 'Enter a valid 10-digit mobile number.')
	customername = models.CharField(max_length = 200)
	mobileno = models.CharField(max_length = 10, primary_key=True, validators=[mobile_validator])
	
	def __str__ (self):
		return self.mobileno

class Products(models.Model):
	productid = models.AutoField(auto_created=True,primary_key=True)
	productname = models.CharField(max_length = 200)
	price = models.DecimalField(max_digits=5,decimal_places=2)
	purchaseprice = models.DecimalField(max_digits=5,decimal_places=2, default = 0)
	inwardqnty = models.IntegerField(default = 0)
	purchasedate = models.DateTimeField(auto_now=True)
	
	def __str__ (self):
		return self.productname

class Invoice(models.Model):
	invoiceid = models.AutoField(auto_created=True,primary_key=True)
	mobile = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True, default=None)
	total = models.DecimalField(max_digits=5,decimal_places=2,default = 0)
	invoicedate = models.DateTimeField(auto_now_add=True)
	
	
	def update_total(self):
		self.total = sum([item.total for item in self.invoicelist.all()])
		self.save()
 
	
	def __str__ (self):
		return f"INV{self.invoiceid}"

class InvoiceList(models.Model):
	invoiceid = models.ForeignKey(Invoice, on_delete=models.CASCADE, null=True, blank=True, default=None, related_name='invoicelist')
	product = models.ForeignKey(Products, on_delete=models.CASCADE)
	quantity = models.IntegerField()
	total = models.DecimalField(max_digits=5,decimal_places=2)	
	
	def save(self, *args, **kwargs):
		
		if self.product.inwardqnty >= self.quantity:
			
			self.total = self.product.price * self.quantity
			self.product.inwardqnty -= self.quantity
			self.product.save()
		else:
			raise ValidationError(f"Only ({self.product.inwardqnty}) available!!!")
		super().save(*args, **kwargs)
		self.invoiceid.update_total()
 
	
	def __str__ (self):
		return f"INV{self.invoiceid}"

class PurchaseList(models.Model):
	purchaseid = models.AutoField(auto_created=True,primary_key=True)
	product = models.ForeignKey(Products, on_delete=models.CASCADE)
	purchaseprice = models.DecimalField(max_digits=5,decimal_places=2, default = 0)
	purchaseqnty = models.IntegerField(default = 0)
	purchasedate = models.DateTimeField(auto_now=True)
	total = models.DecimalField(max_digits=5,decimal_places=2,default=0)

	def save(self, *args, **kwargs):
		self.total = self.purchaseprice * self.purchaseqnty
		super(PurchaseList, self).save(*args, **kwargs) 

	def __str__ (self):
		return f"PUR{self.purchaseid}"
	
	

	

