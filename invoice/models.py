from django.db import models

class Invoice(models.Model):
    invoice_number = models.CharField(max_length=256, unique=True)
    customer_name = models.CharField(max_length=256)
    date = models.DateField()

    def __str__(self):
        return self.invoice_number

class InvoiceDetail(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='details', on_delete=models.CASCADE)
    description = models.CharField(max_length=500)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    line_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.invoice
    
