from django.db import models
from django.utils.safestring import mark_safe


# Create your models here.
# snehajotapota
# 001

class registr(models.Model):
    name=models.CharField(max_length=30)
    email=models.EmailField()
    phone=models.BigIntegerField()
    password=models.CharField(max_length=30)
    address=models.TextField()
    dp=models.ImageField(upload_to='photos')
    gender=models.CharField(max_length=30)
    timestamp=models.DateTimeField(auto_now_add='True')
    def photo(self):
        return mark_safe('<img src={} width="100">'.format(self.dp.url))

    def __str__(self):
        return self.name

class category(models.Model):
    name=models.CharField(max_length=30)
    image=models.ImageField()
    des=models.TextField()
    def __str__(self):
        return self.name


class product(models.Model):
    name=models.CharField(max_length=255)
    stockquantity=models.IntegerField()
    expirydate=models.DateField(auto_now_add='True')
    cat_id=models.ForeignKey(category,on_delete=models.CASCADE)
    price=models.IntegerField()
    des=models.TextField()
    image=models.ImageField(upload_to='photos')
    status=models.CharField(max_length=30)
    dosage=models.TextField()


    def __str__(self):
        return self.name

class cart(models.Model):
    user_id=models.ForeignKey(registr,on_delete=models.CASCADE)
    product_id=models.ForeignKey(product,on_delete=models.CASCADE)
    totalamount=models.FloatField()
    quantity=models.IntegerField()
    status=models.BooleanField(default=False)
    orderid=models.IntegerField() # default - 0, update orderid after placing order



class orderdata(models.Model):
    user_id=models.ForeignKey(registr,on_delete=models.CASCADE)
    totalamount=models.FloatField()
    phone=models.BigIntegerField()
    address=models.TextField()
    paymode=models.CharField(max_length= 50)
    status=models.BooleanField(default=True)
    razorpay_order_id=models.CharField(max_length=255,null=True,blank=True)
    timestamp=models.DateTimeField(auto_now_add=True)


class payment(models.Model):
    transaction_id=models.CharField(max_length=30)
    product_id=models.ForeignKey(product,on_delete=models.CASCADE)
    order_id=models.ForeignKey(orderdata,on_delete=models.CASCADE)
    user_id=models.ForeignKey(registr, on_delete=models.CASCADE)
    dateofpayment=models.DateTimeField(auto_now_add='True')
    status=models.CharField(max_length=30)
    amount=models.FloatField()
    paymentmethod=models.CharField(max_length=30)

class feedback(models.Model):
    user_id=models.ForeignKey(registr,on_delete=models.CASCADE)
    product_id=models.ForeignKey(product,on_delete=models.CASCADE)
    rating=models.IntegerField()
    review=models.CharField(max_length=30)
    feedbackdatetime=models.DateTimeField(auto_now_add='True')

class inquiry(models.Model):
    message=models.TextField()
    contact=models.BigIntegerField()
    username=models.CharField(max_length=30)

class contactpage(models.Model):
    Name=models.CharField(max_length=30)
    email=models.EmailField()
    subject=models.CharField(max_length=30)
    phone=models.BigIntegerField()
    message=models.TextField()






















