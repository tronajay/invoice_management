from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from invoice.models import Invoice, InvoiceDetail


class InvoiceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceDetail
        fields = ['description', 'quantity', 'price', 'line_total']

class InvoiceSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    invoice_number = serializers.CharField(
        validators=[UniqueValidator(queryset=Invoice.objects.all())]
    )
    customer_name = serializers.CharField()
    date = serializers.DateField()
    details = InvoiceDetailSerializer(many=True)

    class Meta:
        model = Invoice
        fields = ['id', 'invoice_number', 'customer_name', 'date', 'details']

    def create(self, validated_data):
        invoice_details = validated_data.pop('details')
        invoice_obj = Invoice.objects.create(**validated_data)
        for detail in invoice_details:
            InvoiceDetail.objects.create(invoice=invoice_obj, **detail)
        return invoice_obj

    def update(self, instance, validated_data):
        invoice_details = validated_data.pop('details')
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()

        # Update the InvoiceDetails
        instance.details.all().delete()  # Clear existing details
        for detail in invoice_details:
            InvoiceDetail.objects.create(invoice=instance, **detail)
        return instance