from django.contrib import admin

from myapp.models import *

from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle


# Register your models here.

def export_to_pdf(modeladmin, request, queryset):
   # Create a new PDF
   response = HttpResponse(content_type='application/pdf')
   response['Content-Disposition'] = 'attachment; filename="report.pdf"'

   # Generate the report using ReportLab
   doc = SimpleDocTemplate(response, pagesize=letter)

   elements = []

   # Define the style for the table
   style = TableStyle([
       ('BACKGROUND', (0,0), (-1,0), colors.grey),
       ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
       ('ALIGN', (0,0), (-1,-1), 'CENTER'),
       ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
       ('FONTSIZE', (0,0), (-1,0), 14),
       ('BOTTOMPADDING', (0,0), (-1,0), 12),
       ('BACKGROUND', (0,1), (-1,-1), colors.beige),
       ('GRID', (0,0), (-1,-1), 1, colors.black),
   ])

   # Create the table headers
   headers = ['UserName', 'UserEmail', 'Phone','Address', 'Gender']

   # Create the table data
   data = []
   for obj in queryset:
       data.append([obj.name, obj.email, obj.phone,obj.address,obj.gender])

   # Create the table
   t = Table([headers] + data, style=style)

   # Add the table to the elements array
   elements.append(t)

   # Build the PDF document
   doc.build(elements)

   return response

export_to_pdf.short_description = "Export to PDF"

class showregistration(admin.ModelAdmin):
    list_display = ['name','email','phone','password','address','dp','photo','gender']
    actions = [export_to_pdf]

admin.site.register(registr,showregistration)

class showcategory(admin.ModelAdmin):
    list_display = ['id','name','image','des',]

admin.site.register(category, showcategory)


class showproduct(admin.ModelAdmin):
    list_display = ['id','name','stockquantity','expirydate','cat_id','price','des','image','status','dosage']

admin.site.register(product, showproduct)


class showcart(admin.ModelAdmin):
    list_display = ['id','user_id','product_id','totalamount','quantity','status','orderid']

admin.site.register(cart,showcart)


class showorder(admin.ModelAdmin):
    list_display = ['id','user_id','totalamount','phone','address','paymode','timestamp','status','razorpay_order_id']
    actions = [export_to_pdf]

admin.site.register(orderdata, showorder)


class showpayment(admin.ModelAdmin):
    list_display = ['id','transaction_id','product_id','order_id','user_id','dateofpayment','status','amount','paymentmethod']

admin.site.register(payment, showpayment)


class showfeedback(admin.ModelAdmin):
    list_display = ['id','user_id','product_id','rating','review','feedbackdatetime']

admin.site.register(feedback, showfeedback)


class showinquiry(admin.ModelAdmin):
    list_display = ['id','message','contact','username']

admin.site.register(inquiry,showinquiry)

class showconttact(admin.ModelAdmin):
    list_display = ['id','Name','email','subject','phone','message']

admin.site.register(contactpage, showconttact)