from django.contrib import admin
from .models import Order, OrderItem, Shipping

# Register your models here.

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

class shippingInline(admin.StackedInline):
    model = Shipping
    raw_id_fields = ['order']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'first_name',
        'last_name',
        'email',
        'paid',
        'created',
        'updated'
    ]
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline, shippingInline]