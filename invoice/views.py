from rest_framework.views import APIView
from rest_framework.response import Response
from invoice.serializers import InvoiceSerializer
from invoice.models import Invoice

class InvoiceAPIView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = InvoiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def put(self, request, *args, **kwargs):
        invoice_obj = Invoice.objects.filter(invoice_number=request.data.get('invoice_number')).first()
        if not invoice_obj:
            return Response({'error': 'No Existing Invoice Found'}, status=400)
        serializer = InvoiceSerializer(invoice_obj, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)