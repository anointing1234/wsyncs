from django.contrib import admin
from unfold.admin import ModelAdmin
from unfold.decorators import display, action
from django.utils.html import format_html
from .models import Account, WalletKeyPhrase

@admin.register(Account)
class AccountAdmin(ModelAdmin):
    list_display = ('email', 'username', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('email', 'username')
    readonly_fields = ('password',)
    fieldsets = (
        (None, {
            'fields': ('email', 'username', 'password')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
    )
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions')

    @display(description="Email")
    def email(self, obj):
        return obj.email

    @display(description="Username")
    def username(self, obj):
        return obj.username

@admin.register(WalletKeyPhrase)
class WalletKeyPhraseAdmin(ModelAdmin):
    list_display = ('wallet_type', 'formatted_key_phrase', 'copy_key_phrase_action', 'created_at', 'updated_at')
    list_filter = ('wallet_type', 'created_at')
    search_fields = ('wallet_type', 'key_phrase')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('wallet_type', 'key_phrase')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    ordering = ('wallet_type',)

    @display(description="Key Phrase")
    def formatted_key_phrase(self, obj):
        words = obj.key_phrase.split()
        numbered_words = [f"{i+1}. {word}" for i, word in enumerate(words)]
        return "\n".join(numbered_words) if words else "No key phrase"

    @display(description="Actions")
    @action(description="Copy Key Phrase")
    def copy_key_phrase_action(self, obj):
        return format_html(
            '<button class="inline-flex items-center px-6 py-3 bg-blue-600 text-white text-base font-semibold rounded-lg '
            'hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 '
            'transition-colors duration-200" '
            'onclick="navigator.clipboard.writeText(\'{}\'); '
            'this.innerText=\'Copied!\'; setTimeout(() => this.innerText=\'Copy Key Phrase\', 2000);" '
            'style="min-width: 160px;">Copy Phrase</button>',
            obj.key_phrase
        )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('key_phrase',)
        return self.readonly_fields