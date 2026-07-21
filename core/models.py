from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Кеңейтилген пайдаланыўшы модели.
    Роллер: user (клиент), manager (менеджер), admin (админ).
    """
    ROLE_CHOICES = [
        ('user', 'Пайдаланыўшы'),
        ('manager', 'Менеджер'),
        ('admin', 'Админ'),
    ]
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Телефон номер'
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='user',
        verbose_name='Роль'
    )
    address = models.TextField(
        blank=True,
        null=True,
        verbose_name='Мекан-жайы'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дизимнен өткен ўақты')

    def is_manager(self):
        return self.role == 'manager'

    def is_admin_user(self):
        return self.role == 'admin'

    def is_regular_user(self):
        return self.role == 'user'

    class Meta:
        verbose_name = 'Пайдаланыўшы'
        verbose_name_plural = 'Пайдаланыўшылар'

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"


class Product(models.Model):
    """
    Күн панели өниминиң модели.
    """
    CATEGORY_CHOICES = [
        ('panel', 'Күн панели'),
        ('battery', 'Батарея'),
        ('inverter', 'Инвертор'),
        ('kit', 'Толық жынаят'),
        ('other', 'Басқа'),
    ]
    title_kk = models.CharField(max_length=200, verbose_name='Аты (КҚ)')
    description_kk = models.TextField(verbose_name='Баянлама (КҚ)')
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='panel',
        verbose_name='Категория'
    )
    price = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        verbose_name='Баҳасы (сум)'
    )
    power_kw = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Қуўаты (кВт)'
    )
    image = models.ImageField(
        upload_to='products/',
        null=True,
        blank=True,
        verbose_name='Сүрет'
    )
    is_active = models.BooleanField(default=True, verbose_name='Жарамлы')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Қосылған ўақты')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Өзгертилген ўақты')

    class Meta:
        verbose_name = 'Өним'
        verbose_name_plural = 'Өнимлер'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title_kk} — {self.price:,} сум"


class Order(models.Model):
    """
    Заказ модели.
    """
    STATUS_CHOICES = [
        ('new', 'Жаңа'),
        ('accepted', 'Қабыл алынды'),
        ('contacted', 'Клиент пенен байланысылды'),
        ('scheduled', 'Монтаж белгиленди'),
        ('installing', 'Орнатылмақта'),
        ('completed', 'Жуўмақланды'),
        ('cancelled', 'Бийкар етилди'),
    ]

    STATUS_KK = {
        'new': 'Жаңа',
        'accepted': 'Қабыл алынды',
        'contacted': 'Клиент пенен байланысылды',
        'scheduled': 'Монтаж белгиленди',
        'installing': 'Орнатылмақта',
        'completed': 'Жуўмақланды',
        'cancelled': 'Бийкар етилди',
    }

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Пайдаланыўшы'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        related_name='orders',
        verbose_name='Өним'
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name='Саны')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name='Статус'
    )
    notes = models.TextField(blank=True, null=True, verbose_name='Ескертпелер')
    manager_notes = models.TextField(blank=True, null=True, verbose_name='Менеджер ескертпеси')
    address = models.TextField(blank=True, null=True, verbose_name='Орнатыў мекан-жайы')
    total_price = models.DecimalField(
        max_digits=14,
        decimal_places=0,
        null=True,
        blank=True,
        verbose_name='Жәми баҳасы'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Жасалған ўақты')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Өзгертилген ўақты')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказлар'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if self.product and not self.total_price:
            self.total_price = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def get_status_kk(self):
        return self.STATUS_KK.get(self.status, self.status)

    def __str__(self):
        return f"Заказ #{self.pk} — {self.user} — {self.get_status_kk()}"


class ContactMessage(models.Model):
    """
    Байланыс формасы арқалы жиберилген хабарлар.
    """
    name = models.CharField(max_length=100, verbose_name='Аты-жөни')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    message = models.TextField(verbose_name='Хабар')
    is_read = models.BooleanField(default=False, verbose_name='Оқылды')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Жиберилген ўақты')

    class Meta:
        verbose_name = 'Байланыс хабары'
        verbose_name_plural = 'Байланыс хабарлары'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} — {self.phone}"
