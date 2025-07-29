from django.db import models
from orders.models import Order

class Payment(models.Model):
    order = models.OneToOneField(Order, related_name='payment', on_delete=models.CASCADE)
    authority = models.CharField(max_length=255)
    ref_id = models.CharField(max_length=255, blank=True, null=True)
    status = models.IntegerField(default=0)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Payment for Order {self.order.id}"
