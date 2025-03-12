from django.db import models
from django.contrib.auth.models import User


CATEGORY_CHOICE=(
    ('Wo', 'Women'),
    ('Me', 'Men'),
    ('Ki', 'Kids'),
    ('El', 'Electonics'),
    ('Cel', 'Celphone'),
)


class Product(models.Model):
    
    title=models.CharField(max_length=200)
    selling_price=models.FloatField()
    discount_price=models.FloatField()
    description=models.TextField()
    composition=models.TextField(default='')
    prodapp=models.TextField(default='')
    category=models.CharField(choices=CATEGORY_CHOICE,max_length=200)
    product_image=models.ImageField()


    def __str__(self):
        return self.title


class Customer(models.Model):
    STATE_CHOICE=(
    ('dodoma','dodoma'),
    ('mbeya','mbeya'),
     ('rukwa','rukwa'),
     ('arusha','arusha'),
     ('kilimanjaro','kilimanjaro'),
     ('dar es salaam','dar es saalam'),
     ('singida','singida'),
     ('songea','songea'),
     ('iringa','iringa'),
     ('morogoro','morogoro'),
     ('mwanza','mwanza'),
     ('kagera','kagera'),
     ('bukoba','bukoba'),
      ('songwe','songwe'),
      ('tabora','tabora'),
      ('njombe','njombe'),
      ('songwe','songwe'),
      ('kagera','kagera'),
      ('moshi','moshi'),
      ('shinyanga','shinyanga'),
      ('tanga','tanga'),
      ('musoma','musuma'),
      ('geita','geita'),

)

    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    locality=models.CharField(max_length=200)
    country=models.CharField(max_length=200, default="Tanzania")
    mobile=models.IntegerField(default=0)
    zipcode=models.IntegerField()
    city=models.CharField(choices=STATE_CHOICE,max_length=200)
    

    def __str__(self):
        return self.name


class Cart(models.Model):
     user=models.ForeignKey(User,on_delete=models.CASCADE)
     product=models.ForeignKey(Product,on_delete=models.CASCADE)
     quantity=models.PositiveIntegerField(default=1)

     @property
     def total_cost(self):
        return self.quantity * self.product.discount_price
     


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('cash_on_delivery', 'Cash on Delivery'),
        ('online_payment', 'Online Payment'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='online_payment')
    paid = models.BooleanField(default=False)
    payment_status = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Payment of {self.amount} for {self.user.username}"


class Order(models.Model):
    STATUS_CHOICE = (
        ('accepted', 'accepted'),
        ('packed', 'packed'),
        ('On the way', 'On the way'),
        ('Delivered', 'Delivered'),
        ('cancel', 'cancel'),
        ('pending', 'pending'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=1)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICE, default='pending')
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, default='')

    @property
    def total_cost(self):
        return self.quantity * self.product.discount_price
    
