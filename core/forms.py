from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser, Order, Product, ContactMessage


class RegisterForm(forms.ModelForm):
    """Дизимнен өтиў формасы"""
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Парольды киргизиң'}),
        label='Пароль',
        min_length=6
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Паролды қайталаң'}),
        label='Паролды қайталаң'
    )
    phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': '+998 XX XXX XX XX'}),
        label='Телефон номер'
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'phone', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Логин (пайдаланыўшы аты)'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Атыңыз'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Фамилияңыз'}),
            'email': forms.EmailInput(attrs={'placeholder': 'email@example.com'}),
        }
        labels = {
            'username': 'Логин',
            'first_name': 'Аты',
            'last_name': 'Фамилиясы',
            'email': 'Email',
        }

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password')
        p2 = cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('Парольлар дурыс емес. Қайтадан сайлаңыз.')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.phone = self.cleaned_data.get('phone', '')
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    """Кириў формасы"""
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Логин'}),
        label='Логин'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}),
        label='Пароль'
    )


class OrderForm(forms.ModelForm):
    """Заказ бериў формасы"""
    class Meta:
        model = Order
        fields = ['product', 'quantity', 'address', 'notes']
        widgets = {
            'quantity': forms.NumberInput(attrs={'min': 1, 'max': 100}),
            'address': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Орнатыў мекан-жайын жазыңыз...'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Қосымша ескертпелер...'}),
        }
        labels = {
            'product': 'Өним',
            'quantity': 'Саны',
            'address': 'Мекан-жайы',
            'notes': 'Ескертпелер',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.filter(is_active=True)
        self.fields['product'].empty_label = '— Өнимди сайлаңыз —'


class ProductForm(forms.ModelForm):
    """Өним қосыў/өзгертиў формасы (Админ ушын)"""
    class Meta:
        model = Product
        fields = ['title_kk', 'description_kk', 'category', 'price', 'power_kw', 'image', 'is_active']
        widgets = {
            'title_kk': forms.TextInput(attrs={'placeholder': 'Өним аты'}),
            'description_kk': forms.Textarea(attrs={'rows': 4}),
            'price': forms.NumberInput(attrs={'placeholder': 'Баҳасы (сум)'}),
            'power_kw': forms.NumberInput(attrs={'placeholder': 'мыс: 5.00'}),
        }
        labels = {
            'title_kk': 'Аты (КҚ)',
            'description_kk': 'Баянлама (КҚ)',
            'category': 'Категория',
            'price': 'Баҳасы (сум)',
            'power_kw': 'Қуўаты (кВт)',
            'image': 'Сүрет',
            'is_active': 'Жарамлы',
        }


class ManagerOrderUpdateForm(forms.ModelForm):
    """Менеджер заказ статусын өзгертиў формасы"""
    class Meta:
        model = Order
        fields = ['status', 'manager_notes']
        labels = {
            'status': 'Статус',
            'manager_notes': 'Менеджер ескертпеси',
        }
        widgets = {
            'manager_notes': forms.Textarea(attrs={'rows': 3}),
        }


class ProfileUpdateForm(forms.ModelForm):
    """Профилди өзгертиў формасы"""
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'phone', 'email', 'address']
        labels = {
            'first_name': 'Аты',
            'last_name': 'Фамилиясы',
            'phone': 'Телефон',
            'email': 'Email',
            'address': 'Мекан-жайы',
        }
        widgets = {
            'address': forms.Textarea(attrs={'rows': 2}),
        }


class ContactForm(forms.ModelForm):
    """Байланыс формасы"""
    class Meta:
        model = ContactMessage
        fields = ['name', 'phone', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Атыңыз'}),
            'phone': forms.TextInput(attrs={'placeholder': '+998 XX XXX XX XX'}),
            'message': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Хабарыңызды жазыңыз...'}),
        }
        labels = {
            'name': 'Аты-жөни',
            'phone': 'Телефон номер',
            'message': 'Хабар',
        }


class AddManagerForm(forms.ModelForm):
    """Жаңа менеджер қосыў формасы (Админ ушын)"""
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}),
        label='Пароль',
        min_length=6
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'phone', 'email']
        labels = {
            'username': 'Логин',
            'first_name': 'Аты',
            'last_name': 'Фамилиясы',
            'phone': 'Телефон',
            'email': 'Email',
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.role = 'manager'
        if commit:
            user.save()
        return user
