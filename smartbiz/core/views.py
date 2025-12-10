from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.core.serializers.json import DjangoJSONEncoder
from functools import wraps
import json
from .models import Product, Sale, Subscription, SubscriptionPlan
from .utils import subscription_required


@login_required
@subscription_required
def dashboard(request):
    from datetime import timedelta
    from django.db.models import Sum, Count, Q
    
    today = timezone.now().date()
    seven_days_ago = today - timedelta(days=7)
    thirty_days_ago = today - timedelta(days=30)
    
    # Today's sales
    sales_today = Sale.objects.filter(user=request.user, created_at__date=today)
    total_today = sales_today.aggregate(Sum('total_price'))['total_price__sum'] or 0
    
    # This week's sales (last 7 days)
    sales_week = Sale.objects.filter(user=request.user, created_at__date__gte=seven_days_ago)
    total_week = sales_week.aggregate(Sum('total_price'))['total_price__sum'] or 0
    
    # This month's sales (last 30 days)
    sales_month = Sale.objects.filter(user=request.user, created_at__date__gte=thirty_days_ago)
    total_month = sales_month.aggregate(Sum('total_price'))['total_price__sum'] or 0
    
    # All time sales
    all_sales = Sale.objects.filter(user=request.user)
    total_all_time = all_sales.aggregate(Sum('total_price'))['total_price__sum'] or 0
    all_time_transactions = all_sales.count()
    
    # Products metrics
    products = Product.objects.filter(user=request.user)
    low_stock_count = products.filter(quantity__lt=10).count()
    out_of_stock = products.filter(quantity=0).count()
    
    # Top selling products
    top_products = Sale.objects.filter(user=request.user).values('product__name').annotate(
        total_sold=Sum('quantity_sold'),
        revenue=Sum('total_price')
    ).order_by('-revenue')[:5]
    
    # Daily sales data for chart (last 7 days)
    daily_sales = {}
    for i in range(7):
        date = today - timedelta(days=6-i)
        daily_sales[date.strftime('%a')] = Sale.objects.filter(
            user=request.user,
            created_at__date=date
        ).aggregate(Sum('total_price'))['total_price__sum'] or 0
    
    # Sales trends
    sales_count_today = sales_today.count()
    sales_count_week = sales_week.count()
    avg_sale_value = total_week / sales_count_week if sales_count_week > 0 else 0
    
    # Calculate healthy stock (not low, not out)
    in_stock_count = products.count() - low_stock_count - out_of_stock
    stock_health_percent = (in_stock_count / products.count() * 100) if products.count() > 0 else 0
    
    # Daily average
    daily_average = (total_week - total_today) / 6 if total_week > total_today else 0
    
    # Convert daily_sales to JSON for JavaScript
    daily_sales_json = json.dumps(daily_sales, cls=DjangoJSONEncoder)
    
    context = {
        "sales_today": sales_today,
        "total_today": int(total_today),
        "total_week": int(total_week),
        "total_month": int(total_month),
        "total_all_time": int(total_all_time),
        "all_time_transactions": all_time_transactions,
        "products": products,
        "low_stock_count": low_stock_count,
        "out_of_stock": out_of_stock,
        "in_stock_count": in_stock_count,
        "stock_health_percent": int(stock_health_percent),
        "top_products": top_products,
        "daily_sales": daily_sales_json,
        "sales_count_today": sales_count_today,
        "sales_count_week": sales_count_week,
        "avg_sale_value": int(avg_sale_value),
        "daily_average": int(daily_average),
    }
    return render(request, "core/dashboard.html", context)


@login_required
@subscription_required
def product_list(request):
    products = Product.objects.filter(user=request.user)
    return render(request, "core/product_list.html", {"products": products})


@login_required
@subscription_required
def product_create(request):
    if request.method == "POST":
        name = request.POST.get("name")
        quantity = request.POST.get("quantity") or 0
        buying_price = request.POST.get("buying_price")
        selling_price = request.POST.get("selling_price")

        Product.objects.create(
            user=request.user,
            name=name,
            quantity=int(quantity),
            buying_price=buying_price,
            selling_price=selling_price,
        )
        return redirect("product_list")

    return render(request, "core/product_form.html")


@login_required
@subscription_required
def product_edit(request, product_id):
    product = get_object_or_404(Product, id=product_id, user=request.user)

    if request.method == "POST":
        product.name = request.POST.get("name")
        product.quantity = int(request.POST.get("quantity") or 0)
        product.buying_price = request.POST.get("buying_price")
        product.selling_price = request.POST.get("selling_price")
        product.save()
        return redirect("product_list")

    return render(request, "core/product_form.html", {"product": product})


@login_required
@subscription_required
def product_delete(request, product_id):
    product = get_object_or_404(Product, id=product_id, user=request.user)

    if request.method == "POST":
        product.delete()
        return redirect("product_list")

    return render(request, "core/product_confirm_delete.html", {"product": product})


@login_required
@subscription_required
def record_sale(request, product_id):
    product = get_object_or_404(Product, id=product_id, user=request.user)

    if request.method == "POST":
        quantity_sold = int(request.POST.get("quantity_sold") or 0)
        if quantity_sold > 0 and quantity_sold <= product.quantity:
            total_price = quantity_sold * product.selling_price

            Sale.objects.create(
                user=request.user,
                product=product,
                quantity_sold=quantity_sold,
                total_price=total_price,
            )

            product.quantity -= quantity_sold
            product.save()

            return redirect("dashboard")

    return render(request, "core/record_sale.html", {"product": product})


@login_required
def subscription_required_view(request):
    return render(request, "core/subscription_required.html")


@login_required
def subscription_expired_view(request):
    return render(request, "core/subscription_expired.html")


@login_required
@subscription_required
def sales_history(request):
    sales = Sale.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "core/sales_history.html", {"sales": sales})


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            return render(request, "core/register.html", {"error": "Passwords do not match"})

        if User.objects.filter(username=username).exists():
            return render(request, "core/register.html", {"error": "Username already exists"})

        user = User.objects.create_user(username=username, email=email, password=password1)
        login(request, user)
        return redirect("onboarding")

    return render(request, "core/register.html")


@login_required
def onboarding(request):
    # Check if user already has a subscription
    if hasattr(request.user, 'subscription'):
        return redirect("dashboard")
    
    return render(request, "core/onboarding.html")


@login_required
def subscription_plans(request):
    # If user already has an active subscription, redirect to dashboard
    if hasattr(request.user, 'subscription') and request.user.subscription.is_current():
        return redirect("dashboard")
    
    plans = SubscriptionPlan.objects.all()
    user_subscription = getattr(request.user, 'subscription', None)
    
    context = {
        "plans": plans,
        "user_subscription": user_subscription,
    }
    return render(request, "core/subscription_plans.html", context)


@login_required
def renew_subscription(request, plan_id):
    plan = get_object_or_404(SubscriptionPlan, id=plan_id)
    
    if request.method == "POST":
        today = timezone.now().date()
        end_date = today + timezone.timedelta(days=plan.duration_days)
        
        # Update or create subscription
        subscription, created = Subscription.objects.update_or_create(
            user=request.user,
            defaults={
                "plan": plan,
                "start_date": today,
                "end_date": end_date,
                "is_active": True,
            }
        )
        
        return redirect("dashboard")
    
    context = {"plan": plan}
    return render(request, "core/renew_subscription.html", context)


@login_required
def subscription_status(request):
    subscription = getattr(request.user, 'subscription', None)
    context = {"subscription": subscription}
    return render(request, "core/subscription_status.html", context)


def landing_page(request):
    """Public landing page for non-authenticated users"""
    context = {}
    return render(request, "core/landing.html", context)


# ========== ADMIN VIEWS ==========

def admin_required(view_func):
    """Decorator to require admin/staff access"""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or not (request.user.is_staff or request.user.is_superuser):
            return redirect("login")
        return view_func(request, *args, **kwargs)
    return _wrapped_view


@login_required
@admin_required
def admin_dashboard(request):
    """Admin dashboard with statistics"""
    # Get all users except superusers/staff (business owners)
    business_owners = User.objects.filter(is_staff=False, is_superuser=False)
    total_users = business_owners.count()
    
    # Subscription stats
    total_subscriptions = Subscription.objects.count()
    active_subscriptions = Subscription.objects.filter(is_active=True).count()
    expired_subscriptions = Subscription.objects.filter(is_active=False).count()
    
    # Revenue calculation
    active_subs = Subscription.objects.filter(is_active=True)
    total_revenue = sum(sub.plan.price for sub in active_subs)
    
    # Due subscriptions (ending within 7 days)
    today = timezone.now().date()
    due_date = today + timezone.timedelta(days=7)
    due_subscriptions = Subscription.objects.filter(
        is_active=True,
        end_date__lte=due_date,
        end_date__gte=today
    ).count()
    
    # Inactive users
    inactive_users = business_owners.filter(is_active=False).count()
    
    context = {
        "total_users": total_users,
        "active_users": business_owners.filter(is_active=True).count(),
        "inactive_users": inactive_users,
        "total_subscriptions": total_subscriptions,
        "active_subscriptions": active_subscriptions,
        "expired_subscriptions": expired_subscriptions,
        "total_revenue": total_revenue,
        "due_subscriptions": due_subscriptions,
    }
    return render(request, "core/admin_dashboard.html", context)


@login_required
@admin_required
def admin_users(request):
    """Manage business owner accounts"""
    business_owners = User.objects.filter(is_staff=False, is_superuser=False).prefetch_related('subscription')
    
    # Filter by status
    status_filter = request.GET.get('status', 'all')
    if status_filter == 'active':
        business_owners = business_owners.filter(is_active=True)
    elif status_filter == 'inactive':
        business_owners = business_owners.filter(is_active=False)
    
    # Filter by subscription
    sub_filter = request.GET.get('subscription', 'all')
    if sub_filter == 'active':
        business_owners = business_owners.filter(subscription__is_active=True)
    elif sub_filter == 'expired':
        business_owners = business_owners.filter(subscription__is_active=False)
    elif sub_filter == 'none':
        business_owners = business_owners.filter(subscription__isnull=True)
    
    context = {
        "users": business_owners,
        "status_filter": status_filter,
        "sub_filter": sub_filter,
    }
    return render(request, "core/admin_users.html", context)


@login_required
@admin_required
def admin_subscriptions(request):
    """Manage subscriptions"""
    subscriptions = Subscription.objects.select_related('user', 'plan').order_by('-end_date')
    
    # Filter by status
    status_filter = request.GET.get('status', 'all')
    if status_filter == 'active':
        subscriptions = subscriptions.filter(is_active=True)
    elif status_filter == 'expired':
        subscriptions = subscriptions.filter(is_active=False)
    
    # Filter by due soon
    due_filter = request.GET.get('due', 'no')
    if due_filter == 'yes':
        today = timezone.now().date()
        due_date = today + timezone.timedelta(days=7)
        subscriptions = subscriptions.filter(
            is_active=True,
            end_date__lte=due_date,
            end_date__gte=today
        )
    
    context = {
        "subscriptions": subscriptions,
        "status_filter": status_filter,
        "due_filter": due_filter,
    }
    return render(request, "core/admin_subscriptions.html", context)


@login_required
@admin_required
def toggle_user_status(request, user_id):
    """Toggle user active status"""
    user = get_object_or_404(User, id=user_id, is_staff=False, is_superuser=False)
    
    if request.method == "POST":
        user.is_active = not user.is_active
        user.save()
        return redirect("admin_users")
    
    context = {"user": user}
    return render(request, "core/confirm_action.html", context)


@login_required
@admin_required
def toggle_subscription_status(request, subscription_id):
    """Toggle subscription active status"""
    subscription = get_object_or_404(Subscription, id=subscription_id)
    
    if request.method == "POST":
        subscription.is_active = not subscription.is_active
        subscription.save()
        return redirect("admin_subscriptions")
    
    context = {"subscription": subscription}
    return render(request, "core/confirm_action.html", context)
