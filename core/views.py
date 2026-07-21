from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Count, Sum, Q
from django.utils import timezone
from datetime import timedelta

from .models import CustomUser, Product, Order, ContactMessage
from .forms import (
    RegisterForm, LoginForm, OrderForm, ProductForm,
    ManagerOrderUpdateForm, ProfileUpdateForm,
    ContactForm, AddManagerForm
)
from .decorators import role_required, login_required_custom


# ─────────────────────────────────────────────
# БАС БЕТ
# ─────────────────────────────────────────────

def home(request):
    """Бас бет"""
    products = Product.objects.filter(is_active=True)[:6]
    contact_form = ContactForm()

    if request.method == 'POST' and 'contact_submit' in request.POST:
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            contact_form.save()
            messages.success(request, '✅ Хабарыңыз жиберилди! Тезде байланысамыз.')
            return redirect('home')

    context = {
        'products': products,
        'contact_form': contact_form,
        'total_orders': Order.objects.filter(status='completed').count(),
        'total_clients': CustomUser.objects.filter(role='user').count(),
    }
    return render(request, 'home.html', context)


def products_list(request):
    """Барлық өнимлер"""
    category = request.GET.get('category', '')
    products = Product.objects.filter(is_active=True)
    if category:
        products = products.filter(category=category)
    return render(request, 'products.html', {'products': products, 'category': category})


# ─────────────────────────────────────────────
# АУТЕНТИФИКАЦИЯ
# ─────────────────────────────────────────────

def register_view(request):
    """Дизимнен өтиў"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'🎉 Хош келдиңиз, {user.first_name or user.username}!')
            return redirect('dashboard')
    return render(request, 'auth/register.html', {'form': form})


def login_view(request):
    """Кириў"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Хош келдиңиз, {user.first_name or user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Логин ямаса пароль нотоғры.')
    return render(request, 'auth/login.html', {'form': form})


def logout_view(request):
    """Шығыў"""
    logout(request)
    messages.info(request, 'Сиз системадан шықтыңыз.')
    return redirect('home')


def dashboard_redirect(request):
    """Рол бойынша дашбоардқа бурыў"""
    if not request.user.is_authenticated:
        return redirect('login')
    role = request.user.role
    if role == 'admin':
        return redirect('admin_dashboard')
    elif role == 'manager':
        return redirect('manager_dashboard')
    else:
        return redirect('user_dashboard')


# ─────────────────────────────────────────────
# ПАЙДАЛАНЫЎШЫ КАБИНЕТИ
# ─────────────────────────────────────────────

@login_required_custom
def user_dashboard(request):
    """Пайдаланыўшы бас беті"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')[:5]
    order_stats = {
        'total': Order.objects.filter(user=request.user).count(),
        'new': Order.objects.filter(user=request.user, status='new').count(),
        'completed': Order.objects.filter(user=request.user, status='completed').count(),
    }
    return render(request, 'user/dashboard.html', {
        'orders': orders,
        'order_stats': order_stats,
        'products': Product.objects.filter(is_active=True)[:4],
    })


@login_required_custom
def user_orders(request):
    """Барлық заказларым"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'user/orders.html', {'orders': orders})


@login_required_custom
def user_order_create(request):
    """Жаңа заказ жасаў"""
    form = OrderForm()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            messages.success(request, '✅ Заказыңыз қабыл алынды!')
            return redirect('user_orders')
    return render(request, 'user/order_create.html', {'form': form})


@login_required_custom
def user_profile(request):
    """Профилди өзгертиў"""
    form = ProfileUpdateForm(instance=request.user)
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Профилиңиз жаңаланды!')
            return redirect('user_profile')
    return render(request, 'user/profile.html', {'form': form})


# ─────────────────────────────────────────────
# МЕНЕДЖЕР ПАНЕЛИ
# ─────────────────────────────────────────────

@role_required('manager', 'admin')
def manager_dashboard(request):
    """Менеджер бас беті"""
    orders = Order.objects.select_related('user', 'product').order_by('-created_at')
    stats = {
        'new': orders.filter(status='new').count(),
        'in_progress': orders.filter(status__in=['accepted', 'contacted', 'scheduled', 'installing']).count(),
        'completed': orders.filter(status='completed').count(),
        'total': orders.count(),
    }
    recent_orders = orders[:10]
    return render(request, 'manager/dashboard.html', {
        'orders': recent_orders,
        'stats': stats,
    })


@role_required('manager', 'admin')
def manager_orders(request):
    """Барлық заказларды басқарыў"""
    status_filter = request.GET.get('status', '')
    orders = Order.objects.select_related('user', 'product').order_by('-created_at')
    if status_filter:
        orders = orders.filter(status=status_filter)
    return render(request, 'manager/orders.html', {
        'orders': orders,
        'status_filter': status_filter,
        'status_choices': Order.STATUS_CHOICES,
    })


@role_required('manager', 'admin')
def manager_order_update(request, pk):
    """Заказ статусын өзгертиў"""
    order = get_object_or_404(Order, pk=pk)
    form = ManagerOrderUpdateForm(instance=order)
    if request.method == 'POST':
        form = ManagerOrderUpdateForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, f'✅ Заказ #{pk} статусы жаңаланды!')
            return redirect('manager_orders')
    return render(request, 'manager/order_update.html', {'form': form, 'order': order})


@role_required('manager', 'admin')
def manager_clients(request):
    """Клиентлер тизими"""
    clients = CustomUser.objects.filter(role='user').annotate(
        orders_count=Count('orders')
    ).order_by('-created_at')
    return render(request, 'manager/clients.html', {'clients': clients})


# ─────────────────────────────────────────────
# АДМИН ПАНЕЛИ
# ─────────────────────────────────────────────

@role_required('admin')
def admin_dashboard(request):
    """Админ бас беті — статистика"""
    now = timezone.now()
    last_30_days = now - timedelta(days=30)

    stats = {
        'total_users': CustomUser.objects.filter(role='user').count(),
        'total_managers': CustomUser.objects.filter(role='manager').count(),
        'total_products': Product.objects.filter(is_active=True).count(),
        'total_orders': Order.objects.count(),
        'new_orders': Order.objects.filter(status='new').count(),
        'completed_orders': Order.objects.filter(status='completed').count(),
        'monthly_revenue': Order.objects.filter(
            status='completed',
            created_at__gte=last_30_days
        ).aggregate(total=Sum('total_price'))['total'] or 0,
        'unread_messages': ContactMessage.objects.filter(is_read=False).count(),
    }

    recent_orders = Order.objects.select_related('user', 'product').order_by('-created_at')[:5]
    recent_messages = ContactMessage.objects.order_by('-created_at')[:5]

    return render(request, 'admin_panel/dashboard.html', {
        'stats': stats,
        'recent_orders': recent_orders,
        'recent_messages': recent_messages,
    })


@role_required('admin')
def admin_products(request):
    """Өнимлерди басқарыў"""
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'admin_panel/products.html', {'products': products})


@role_required('admin')
def admin_product_create(request):
    """Жаңа өним қосыў"""
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Жаңа өним қосылды!')
            return redirect('admin_products')
    return render(request, 'admin_panel/product_form.html', {'form': form, 'action': 'Қосыў'})


@role_required('admin')
def admin_product_edit(request, pk):
    """Өнимди өзгертиў"""
    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(instance=product)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Өним жаңаланды!')
            return redirect('admin_products')
    return render(request, 'admin_panel/product_form.html', {'form': form, 'action': 'Өзгертиў', 'product': product})


@role_required('admin')
def admin_product_delete(request, pk):
    """Өнимди өшириў"""
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, '🗑️ Өним өшириўди.')
        return redirect('admin_products')
    return render(request, 'admin_panel/product_confirm_delete.html', {'product': product})


@role_required('admin')
def admin_managers(request):
    """Менеджерлер тизими"""
    managers = CustomUser.objects.filter(role='manager').order_by('-created_at')
    return render(request, 'admin_panel/managers.html', {'managers': managers})


@role_required('admin')
def admin_manager_add(request):
    """Жаңа менеджер қосыў"""
    form = AddManagerForm()
    if request.method == 'POST':
        form = AddManagerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Жаңа менеджер қосылды!')
            return redirect('admin_managers')
    return render(request, 'admin_panel/manager_form.html', {'form': form})


@role_required('admin')
def admin_manager_delete(request, pk):
    """Менеджерді өшириў"""
    manager = get_object_or_404(CustomUser, pk=pk, role='manager')
    if request.method == 'POST':
        manager.delete()
        messages.success(request, '🗑️ Менеджер өшириўди.')
        return redirect('admin_managers')
    return render(request, 'admin_panel/manager_confirm_delete.html', {'manager': manager})


@role_required('admin')
def admin_messages(request):
    """Байланыс хабарларын көриў"""
    msgs = ContactMessage.objects.order_by('-created_at')
    ContactMessage.objects.filter(is_read=False).update(is_read=True)
    return render(request, 'admin_panel/messages.html', {'messages_list': msgs})


@role_required('admin')
def admin_all_orders(request):
    """Барлық заказларды басқарыў (Админ)"""
    orders = Order.objects.select_related('user', 'product').order_by('-created_at')
    return render(request, 'admin_panel/orders.html', {'orders': orders})
