from django.shortcuts import render
from openpyxl.styles.fills import PatternFill
from openpyxl.styles.fonts import Font
from openpyxl.workbook.workbook import Workbook
from reportlab.lib.enums import TA_CENTER, TA_LEFT

from .models import Sale


from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from .models import SoldTours


def sale_list(request):
    sales = Sale.objects.all()
    return render(request, 'sales/sale_list.html', {'sales': sales})

def export_pdf(request, pk):
    sale = SoldTours.objects.get(pk=pk)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="SoldTour_{sale.pk}.pdf"'

    doc = SimpleDocTemplate(
        response,
        pagesize=(80 * mm, 250 * mm),  # narrow receipt size
        rightMargin=5,
        leftMargin=5,
        topMargin=10,
        bottomMargin=10
    )

    styles = getSampleStyleSheet()
    elements = []

    # Styles
    title_style = ParagraphStyle(
        name='Title',
        fontSize=12,
        leading=14,
        alignment=TA_CENTER,
        textColor=colors.black,
    )

    normal_style = ParagraphStyle(
        name='Normal',
        fontSize=8,
        leading=10,
        alignment=TA_LEFT
    )

    center_style = ParagraphStyle(
        name='Center',
        fontSize=8,
        alignment=TA_CENTER,
        leading=10
    )

    bold_style = ParagraphStyle(
        name='Bold',
        fontSize=9,
        alignment=TA_LEFT,
        leading=11,
        textColor=colors.black
    )

    # Header
    elements.append(Paragraph("<b>DUBAI TOUR AGENCY</b>", title_style))
    elements.append(Paragraph("SALES RECEIPT", center_style))
    elements.append(Spacer(1, 4))

    # Meta
    elements.append(Paragraph(f"Receipt ID: #{sale.pk}", normal_style))
    elements.append(Paragraph(f"Date: {sale.created_at.strftime('%d-%m-%Y %H:%M')}", normal_style))
    elements.append(Spacer(1, 6))

    # Sale info table
    info_data = [
        ["Tour", str(sale.tour)],
        ["Agent", str(sale.agent)],
        ["Processed At", sale.processed_at.strftime('%Y-%m-%d') if sale.processed_at else "-"],
        ["Description", sale.description or "-"],
        ["Discount", f"{sale.discount}"],
        ["Discount Type", sale.discount_type or "-"],
    ]

    table = Table(info_data, colWidths=[28 * mm, 42 * mm])
    table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('LINEBELOW', (0, 0), (-1, -1), 0.2, colors.grey),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 10))

    # Footer
    footer = Paragraph(
        "Thanks for choosing us!<br/>Contact: support@dubaitour.com",
        center_style
    )
    elements.append(footer)

    doc.build(elements)
    return response


def export_excel(request, pk):
    sale = SoldTours.objects.get(pk=pk)
    wb = Workbook()
    ws = wb.active
    ws.title = "Sold Tour"
    headers = ["Field", "Value"]
    data = [
        ["ID", sale.pk],
        ["Created At", str(sale.created_at)],
        ["Tour", str(sale.tour)],
        ["Agent", str(sale.agent)],
        ["Processed At", str(sale.processed_at)],
        ["Description", sale.description or "-"],
        ["Discount", sale.discount],
        ["Discount Type", sale.discount_type],
    ]
    ws.append(headers)
    for row in data:
        ws.append(row)

    for cell in ws["1:1"]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill(start_color="4F81BD", end_color="4F81BD", fill_type="solid")

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="soldtour_{sale.pk}.xlsx"'
    wb.save(response)
    return response



