from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
import razorpay
from django.db.models import Sum, Q
from django.http import JsonResponse


from myapp.models import *

# Create your views here.
def index(request):
    allprode=product.objects.all()
    context= {
        'alldata':allprode
    }
    return render(request,'index.html',context)

def signup(request):
    return render(request,'sign-up.html')

def insertdata(request):
    uname=request.POST.get('name')
    uemail=request.POST.get('email')
    uphone=request.POST.get('phone')
    upassword=request.POST.get('password')
    uaddress=request.POST.get('address')
    udp=request.FILES['dp']
    ugender=request.POST.get('gender')
    if registr.objects.filter(email=uemail):
        print("Account already exists")
        return render(request,'sign-up.html')
    else:
        insertquery=registr(name=uname,email=uemail,phone=uphone,password=upassword,address=uaddress,dp=udp,gender=ugender)
        insertquery.save()
        messages.success(request,'registeration successfull!!')
        return render(request,'sign-in.html')

def signin(request):
    return render(request, 'sign-in.html')

def verifyuser(request):
    uemail = request.POST.get('name')
    upassword = request.POST.get('password')
    print(uemail)
    print(upassword)
    try:
        userdata = registr.objects.get(email=uemail,password=upassword)
        request.session['login_id']= userdata.id
        request.session['login_email']= userdata.email
        request.session['login_name'] = userdata.name
        request.session.save()
        # messages.success(request,'Login Successfull')
        print('Login Successfull')
        return redirect(index)
    except:
        print('Some Error Occured')
        return render(request,'sign-up.html')

def shop(request):
    allprode = product.objects.all()
    allcat = category.objects.all()

    best_sellers = product.objects.annotate(
        total_sold=Sum('cart__quantity', filter=Q(cart__status=True))
    ).filter(
        total_sold__gt=0
    ).order_by('-total_sold')[:10]  # Get top 10

    context = {
        'alldata': allprode,
        'allcat': allcat,
        'best_sellers': best_sellers,
        'title': 'Best Selling Products'
    }

    return render(request, 'shop.html', context)


def filter_products(request):
    category_id = request.POST.get('category_id')
    allcat = category.objects.all()

    # products = product.objects.all()


    best_sellers = product.objects.annotate(
        total_sold=Sum('cart__quantity', filter=Q(cart__status=True))
    ).filter(
        total_sold__gt=0
    ).order_by('-total_sold')[:10]  # Get top 10
    if category_id:
        products = product.objects.filter(cat_id=category_id)
    else:
        products = product.objects.all()

    return render(request, 'shop.html', {
        'alldata': products,
        'allcat': allcat,
        'best_sellers': best_sellers,
        'title': 'Best Selling Products'})

def productsearch(request):
    query = request.GET.get('q')
    if query:
        results = product.objects.filter(name__icontains=query)
    else:
        results = product.objects.none()

    return render(request, 'shop.html', {
        'alldata': results,
         'query': query})

def logout(request):
    try:
        del request.session['login_id']
        del request.session['login_name']
        del request.session['login_email']
        messages.success(request, 'logout successfull')
        return redirect(index)
    except:
        messages.error(request,'account Does Not Exist')
        return render(request,'sign-up.html')

from django.core.mail import send_mail  # ✅ Make sure this is at the top
import razorpay
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect


def prodetails(request, pid):
    user_id = request.session.get("login_id")
    prodata = product.objects.get(id=pid)

    if request.method == "POST":
        current_user = registr.objects.get(id=user_id)  # ✅ Correctly fetch full user object

        qty = int(request.POST.get("qty"))
        ftotal = int(prodata.price) * qty
        address = request.POST.get("address")
        phone = request.POST.get("phone")
        payment_mode = request.POST.get("paymode")

        if payment_mode == "offline":
            storedata = orderdata.objects.create(
                user_id=current_user,  # ✅ Use full user object
                totalamount=ftotal,
                phone=phone,
                address=address,
                paymode="Offline",
            )

            try:
                send_mail(
                    subject='Order Confirmation - Payment Successful',
                    message=f"Dear {storedata.user_id.name},\n\nYour offline order (Order ID: {storedata.id}) has been successfully placed.\n\nThank you for shopping with us!\n\n- Your Team",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[storedata.user_id.email],
                    fail_silently=False,
                )
                print("Mail sent successfully to:", storedata.user_id.email)
            except Exception as e:
                print("Mail sending error:", e)

            messages.success(request, "Order placed successfully!")
            return redirect("/")

        else:
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY))
            order_amount = int(ftotal) * 100

            razorpay_order = client.order.create({
                "amount": order_amount,
                "currency": "INR",
                "receipt": f"order_rcptid_{user_id}",
                "payment_capture": "1",
            })

            storedata = orderdata.objects.create(
                user_id=current_user,
                totalamount=ftotal,
                phone=phone,
                address=address,
                paymode="Online",
                razorpay_order_id=razorpay_order['id'],
            )

            try:
                send_mail(
                    subject='Payment Successful',
                    message=f"Dear {storedata.user_id.name},\n\nYour payment for Order ID {storedata.id} has been successfully processed. Thank you for choosing us!\n\nBest regards,\nYour Team",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[storedata.user_id.email],
                    fail_silently=False,
                )
                print("Mail sent successfully to:", storedata.user_id.email)
            except Exception as e:
                print("Mail sending error:", e)

            return render(request, "payment.html", {
                "razorpay_order_id": razorpay_order['id'],
                "amount": order_amount,
                "key": settings.RAZORPAY_KEY_ID,
                "currency": "INR",
                'status': True
            })

    context = {
        'singledata': prodata,
        'total': prodata.price,
    }
    return render(request, 'shopdetails.html', context)


def userdata(request):
    try:
        user_id = request.session['login_id']
        if user_id:
            userdata = registr.objects.get(id=user_id)
            print(userdata)
            context = {
                'data': userdata
            }
            return render(request,'userdetails.html',context)

        else:
            messages.error(request, 'Please login first')

            return render(request,'userdetails.html',)

    except:
        messages.error(request,'Error occured')

    return render(request,'userdetails.html')

def editprofile(request):
    uid=request.session['login_id']
    fetchdata=registr.objects.get(id=uid)
    context={
        'data':fetchdata
    }
    return render(request,'editprofile.html',context)


def update(request):
    uname=request.POST.get('name')
    uemail=request.POST.get('email')
    upassword=request.POST.get('password')
    uphone=request.POST.get('phone')
    uaddress=request.POST.get('address')
    udp=request.FILES['dp']
    proid=request.session['login_id']

    obj=registr.objects.get(id=proid)
    obj.name=uname
    obj.email=uemail
    obj.password=upassword
    obj.phone=uphone
    obj.address=uaddress
    obj.dp=udp
    obj.save()
    return redirect(userdata)

def showcart(request):
    user_id = request.session['login_id']
    allcartdata = cart.objects.filter(user_id=user_id,status=0, orderid=0)
    print(allcartdata)
    total=sum(i.totalamount for i in allcartdata)
    return render(request,'cart.html',{'allcartdata':allcartdata,'total':total})

def insertcart(request):
    user_id=request.session['login_id']
    pro_id=request.POST.get('pid')
    qty=request.POST.get('qty')
    amount=request.POST.get('pprice')
    totalamount=float(qty)*float(amount)
    query=cart(user_id=registr(id=user_id),
               product_id=product(id=pro_id),
               quantity=qty,
               totalamount=totalamount,
               status=0,orderid=0,
               )
    query.save()
    messages.success(request,'product added to cart successfully')
    return redirect(shop)

def removecartiteam(request,rid):
    fetchdata=cart.objects.get(id=rid)
    fetchdata.delete()
    messages.success(request,'Product removed from cart successfully')

    return redirect(showcart)

def increase(request,iid):

    fetchdata=cart.objects.get(id=iid)
    fetchdata.quantity+=1
    fetchdata.totalamount+=fetchdata.product_id.price
    fetchdata.save()
    messages.success(request,'Product quantity increased')
    return redirect(showcart)

def decrease(request,did):
    fetchdata=cart.objects.get(id=did)
    if fetchdata.quantity==1:
        fetchdata.delete()
    else:
        fetchdata.quantity-=1
        fetchdata.totalamount-=fetchdata.product_id.price
        fetchdata.save()
    messages.success(request,'Product quantity decreased')
    return redirect(showcart)

from django.core.mail import send_mail
from django.conf import settings

def placeorder(request):
    user_id = request.session["login_id"]
    current_user = registr.objects.get(id=user_id)  # ✅ Correctly fetch full user object

    ftotal = request.POST.get("total")
    address = request.POST.get("address")
    phone = request.POST.get("phone")
    payment_mode = request.POST.get("paymode")

    if payment_mode == "offline":
        storedata = orderdata.objects.create(
            user_id=current_user,
            totalamount=ftotal,
            phone=phone,
            address=address,
            paymode="Offline"
        )

        # Update cart items
        cart_items = cart.objects.filter(user_id=user_id, status=0)
        for i in cart_items:
            i.status = 1
            i.orderid = storedata.id
            i.save()

        # Send email
        try:
            send_mail(
                subject='Order Confirmation - Payment Successful',
                message=f"Dear {current_user.name},\n\nYour offline order (Order ID: {storedata.id}) has been placed successfully.\n\nThank you for shopping with us!\n\n- Your Team",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[current_user.email],
                fail_silently=False,
            )
            print("Email sent to:", current_user.email)
        except Exception as e:
            print("Email sending failed:", e)

        messages.success(request, "Order Placed Successfully")
        return redirect("/")

    else:
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY))
        order_amount = int(float(ftotal) * 100)  # Razorpay needs amount in paise

        razorpay_order = client.order.create({
            "amount": order_amount,
            "currency": "INR",
            "receipt": f"order_rcptid_{user_id}",
            "payment_capture": "1",
        })

        storedata = orderdata.objects.create(
            user_id=current_user,
            totalamount=ftotal,
            phone=phone,
            address=address,
            paymode="Online",
            razorpay_order_id=razorpay_order['id'],
        )

        # Update cart items
        cart_items = cart.objects.filter(user_id=user_id, status=0)
        for item in cart_items:
            item.status = 1
            item.orderid = storedata.id
            item.save()

        # Send email
        try:
            send_mail(
                subject='Payment Successful',
                message=f"Dear {current_user.name},\n\nYour payment for Order ID {storedata.id} has been successfully processed.\n\nThank you for choosing us!\n\nBest regards,\nYour Team",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[current_user.email],
                fail_silently=False,
            )
            print("Email sent to:", current_user.email)
        except Exception as e:
            print("Email sending failed:", e)

        return render(request, "payment.html", {
            "razorpay_order_id": razorpay_order['id'],
            "amount": order_amount,
            "key": settings.RAZORPAY_KEY_ID,
            "currency": "INR",
        })



def payment_success(request):
    return redirect("/")

def manageorder(request):
    uid=request.session['login_id']
    orderdataa=orderdata.objects.filter(user_id=uid,status=1)
    return render(request,'manageorder.html',{'orderdataa':orderdataa})

def orderdetails(request,oid):
    detaildata=cart.objects.filter(orderid=oid)
    total = sum(i.totalamount for i in detaildata)
    return render(request,'orderdetails.html',{'detaildata':detaildata,'total':total})


def best_selling_products(request):
    # Assuming you have a 'sales_count' field in your Product model
    best_sellers = product.objects.filter(status='active').order_by('-sales_count')[:10]

    context = {
        'best_sellers': best_sellers,
        'title': 'Best Selling Products'
    }
    return render(request, 'shop.html', context)


def contactdata(request):
    return render(request,'contact.html')

def contactMessage(request):
    pname = request.POST.get('name')
    pemail = request.POST.get('email')
    psubject = request.POST.get('msg_subject')
    pphone = request.POST.get('phone_number')
    pmesssage = request.POST.get('message')

    insertquery = contactpage(
        Name=pname,
        email=pemail,
        subject=psubject,
        phone=pphone,
        message=pmesssage,
    )
    insertquery.save()
    return redirect(contactdata)

def about(request):
    return render(request,'about.html')


def some_view(request):
    # Get cart count for logged in user
    cart_count = 0
    if request.user.is_authenticated:
        cart_count = cart.objects.filter(user_id=request.user, status=False).count()

    context = {
        'cart_count': cart_count
    }
    return render(request, 'base.html', context)
def get_cart_count(request):
    if request.user.is_authenticated:
        count = cart.objects.filter(user_id=request.user, status=False).count()
        return JsonResponse({'count': count})
    return JsonResponse({'count': 0})
