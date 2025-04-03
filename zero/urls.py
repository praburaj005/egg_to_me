from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('print/', views.print, name = "print"),
    path('addproduct/', views.addproduct, name = "addproduct"),
    path('addcustomer/', views.addcustomer, name = "addcustomer"),
    path('invoice/', views.invoice, name = "invoice"),
    path('purchasedetails/', views.purchasedetails, name = "purchasedetails"),
    path('createinvoice/', views.createinvoice, name = "createinvoice"),
    path('addpurchase/', views.addpurchase, name = "addpurchase"),
    path('createinvoiceid/', views.createinvoiceid, name = "createinvoiceid"),
    path('customer/', views.customer, name = "customer"),
    path('updateproduct/<int:productid>/', views.updateproduct, name = "updateproduct"),
    path('updateinvoice/<int:invoiceid>/', views.updateinvoice, name = "updateinvoice"),
    path('mobilefilter/<int:mobileno>/', views.mobilefilter, name = "mobilefilter"),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('download/', views.download, name='download'),
]