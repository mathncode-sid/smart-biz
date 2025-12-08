from functools import wraps
from django.shortcuts import redirect
from django.utils import timezone
from .models import Product


def subscription_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return redirect("login")

        # Admin users don't need a subscription
        if user.is_staff or user.is_superuser:
            return view_func(request, *args, **kwargs)

        subscription = getattr(user, "subscription", None)
        if subscription is None:
            return redirect("subscription_required")

        today = timezone.now().date()
        if not subscription.is_active or subscription.end_date < today:
            return redirect("subscription_expired")

        return view_func(request, *args, **kwargs)

    return _wrapped_view


def get_notifications(request):
    """Get notifications for the current user"""
    notifications = []
    
    if not request.user.is_authenticated:
        return notifications
    
    # Check for low stock products
    low_stock_products = Product.objects.filter(
        user=request.user,
        quantity__lt=10,
        quantity__gt=0
    ).count()
    
    if low_stock_products > 0:
        notifications.append({
            "type": "warning",
            "message": f"⚠️ You have {low_stock_products} product(s) with low stock!"
        })
    
    # Check for out of stock products
    out_of_stock = Product.objects.filter(
        user=request.user,
        quantity=0
    ).count()
    
    if out_of_stock > 0:
        notifications.append({
            "type": "danger",
            "message": f"❌ You have {out_of_stock} out-of-stock product(s)!"
        })
    
    # Check subscription status
    subscription = getattr(request.user, "subscription", None)
    if subscription:
        today = timezone.now().date()
        days_left = (subscription.end_date - today).days
        
        if 0 <= days_left <= 7:
            notifications.append({
                "type": "info",
                "message": f"ℹ️ Your subscription expires in {days_left} days. Renew now to continue!"
            })
    
    return notifications
