from django.urls import path
from . import views

urlpatterns = [
    # ── Бас бет ──────────────────────────────────
    path('', views.home, name='home'),
    path('products/', views.products_list, name='products_list'),

    # ── Аутентификация ────────────────────────────
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_redirect, name='dashboard'),

    # ── Пайдаланыўшы кабинети ─────────────────────
    path('user/dashboard/', views.user_dashboard, name='user_dashboard'),
    path('user/orders/', views.user_orders, name='user_orders'),
    path('user/orders/new/', views.user_order_create, name='user_order_create'),
    path('user/profile/', views.user_profile, name='user_profile'),

    # ── Менеджер панели ──────────────────────────
    path('manager/', views.manager_dashboard, name='manager_dashboard'),
    path('manager/orders/', views.manager_orders, name='manager_orders'),
    path('manager/orders/<int:pk>/update/', views.manager_order_update, name='manager_order_update'),
    path('manager/clients/', views.manager_clients, name='manager_clients'),

    # ── Админ панели ─────────────────────────────
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/products/', views.admin_products, name='admin_products'),
    path('admin-panel/products/add/', views.admin_product_create, name='admin_product_create'),
    path('admin-panel/products/<int:pk>/edit/', views.admin_product_edit, name='admin_product_edit'),
    path('admin-panel/products/<int:pk>/delete/', views.admin_product_delete, name='admin_product_delete'),
    path('admin-panel/managers/', views.admin_managers, name='admin_managers'),
    path('admin-panel/managers/add/', views.admin_manager_add, name='admin_manager_add'),
    path('admin-panel/managers/<int:pk>/delete/', views.admin_manager_delete, name='admin_manager_delete'),
    path('admin-panel/messages/', views.admin_messages, name='admin_messages'),
    path('admin-panel/orders/', views.admin_all_orders, name='admin_all_orders'),
]
