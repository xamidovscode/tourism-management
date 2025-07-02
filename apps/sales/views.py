from django.http import HttpResponse
from django.shortcuts import render
from reportlab.pdfgen import canvas
from io import BytesIO
from .models import SoldTours, Sale


def export_pdf(request, pk):
    sale = SoldTours.objects.get(pk=pk)

    # Create a PDF buffer
    buffer = BytesIO()
    p = canvas.Canvas(buffer)

    # Simple example content
    p.drawString(100, 800, f"PDF Export for Sale ID: {sale.id}")
    p.drawString(100, 780, f"Tour: {sale.tour}")
    p.drawString(100, 760, f"Agent: {sale.agent}")
    p.drawString(100, 740, f"Processed At: {sale.processed_at}")
    p.drawString(100, 720, f"Description: {sale.description}")

    # Finalize PDF
    p.showPage()
    p.save()

    buffer.seek(0)

    # Return as downloadable file
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=sale_{sale.id}.pdf'
    return response

def export_excel(request, pk):
    sale = SoldTours.objects.get(pk=pk)
    # 👇 replace with your actual export logic
    return HttpResponse(f"Excel export for sale ID {pk}")



def sale_list(request):
    sales = Sale.objects.all()
    return render(request, 'sales/sale_list.html', {'sales': sales})
