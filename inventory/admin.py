from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import *

# Register your models here.


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)


class RequestServerAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'implementation_date', 'customer', 'is_approved', 'remark')


class PcAdmin(admin.ModelAdmin):
    list_display = ('pc_number', 'motherboard', 'hdd', 'ssd', 'ram1', 'ram2', 'get_ram_size')


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Principal)
admin.site.register(Distributor)
admin.site.register(Customer)
admin.site.register(Pc, PcAdmin)
admin.site.register(Psu)
admin.site.register(Motherboard)
admin.site.register(Ram)
admin.site.register(Hdd)
admin.site.register(Ssd)
admin.site.register(RequestServer, RequestServerAdmin)
