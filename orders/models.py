from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Order(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    coupon = models.ForeignKey('coupons.Coupon', related_name='orders', null=True, blank=True, on_delete=models.SET_NULL)
    discount = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]

    def __str__(self):
        return f"Order {self.id}"
    
    def get_total_cost(self):
        total_cost = self.get_total_cost_befor_discount()
        discount = self.get_discount()
        return total_cost - discount
    
    def get_total_cost_befor_discount(self):
        return sum(item.get_cost() for item in self.items.all())
    
    def get_discount(self):
        if self.discount:
            return self.get_total_cost_befor_discount() * (self.discount / 100)
        return 0
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('shop.Product', related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"OrderItem {self.id}"
    
    def get_cost(self):
        return self.price * self.quantity
    

class Shipping(models.Model):
    DURATION_CHOICES = [
        ('standard', 'Standard'),
        ('express', 'Express'),
    ]
    order = models.OneToOneField(Order, related_name='shipping', on_delete=models.CASCADE)
    shipping_duration = models.CharField(max_length=10, choices=DURATION_CHOICES, default='standard')
    address = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=50)
    shipping_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return f"Shipping for Order {self.order.id}"