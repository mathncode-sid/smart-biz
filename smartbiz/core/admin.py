from django.contrib import admin
from .models import SubscriptionPlan, Subscription, Product, Sale

admin.site.register(SubscriptionPlan)
admin.site.register(Subscription)
admin.site.register(Product)
admin.site.register(Sale)
