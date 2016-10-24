from django import forms
from django.contrib import admin

from EuLevo.site import register
from .models import CoreUser, Profile, UserPoint


class ProfileInline(admin.StackedInline):
    model = Profile
    verbose_name = 'perfil'


@register(CoreUser)
class UserAdmin(admin.ModelAdmin):
    inlines = (ProfileInline,)

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'password':
            return db_field.formfield(widget=forms.PasswordInput())
        return super(UserAdmin, self).formfield_for_dbfield(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.set_password(obj.password)
        super(UserAdmin, self).save_model(request, obj, form, change)


@register(UserPoint)
class UserPointAdmin(admin.ModelAdmin):
    pass

