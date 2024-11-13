from django.urls import path
from invoice.views import InvoiceAPIView

urlpatterns = [
    path('api/invoices/', InvoiceAPIView.as_view()),
]
