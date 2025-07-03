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

    # PDF settings
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="SoldTour_{sale.pk}.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4,
                            rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)

    styles = getSampleStyleSheet()
    elements = []

    # Custom styles
    title_style = ParagraphStyle(
        name='TitleStyle',
        parent=styles['Title'],
        fontSize=16,
        alignment=TA_CENTER,
        textColor=colors.darkblue,
    )

    label_style = ParagraphStyle(
        name='LabelStyle',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_LEFT,
        textColor=colors.black,
    )

    footer_style = ParagraphStyle(
        name='FooterStyle',
        parent=styles['Normal'],
        fontSize=9,
        alignment=TA_CENTER,
        textColor=colors.grey,
    )

    # 🧾 Title
    elements.append(Paragraph("🏝 <b>DUBAI TOUR AGENCY</b>", title_style))
    elements.append(Paragraph("<b>SALES RECEIPT</b>", title_style))
    elements.append(Spacer(1, 10))

    # 🔖 Meta info (ID, Date)
    elements.append(Paragraph(f"<b>Receipt ID:</b> #{sale.pk}", label_style))
    elements.append(Paragraph(f"<b>Date:</b> {sale.created_at.strftime('%d-%m-%Y %H:%M')}", label_style))
    elements.append(Spacer(1, 10))

    # 📋 Main Info Table
    data = [
        ["Tour:", str(sale.tour)],
        ["Agent:", str(sale.agent)],
        ["Processed At:", sale.processed_at.strftime('%Y-%m-%d') if sale.processed_at else "-"],
        ["Description:", sale.description or "-"],
        ["Discount:", f"{sale.discount}"],
        ["Discount Type:", sale.discount_type or "-"],
    ]

    table = Table(data, colWidths=[40 * mm, 120 * mm])
    table.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 1.2, colors.black),
        ('INNERGRID', (0, 0), (-1, -1), 0.6, colors.grey),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 20))

    # ✅ Footer note
    footer = Paragraph(
        "Thank you for choosing Dubai Tour Agency! <br/> "
        "If you have any questions, contact us at: support@dubaitour.com",
        footer_style
    )
    elements.append(footer)

    # Generate PDF
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



