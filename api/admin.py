from django.contrib import admin
from .models import Gift, Staff, Team, Wishlist


class StaffAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'birth_date', 'sex', 'slack_id')


class GiftAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class WishlistAdmin(admin.ModelAdmin):
    list_display = ('id', 'employee_name')


class TeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'teamlead')


admin.site.register(Gift, GiftAdmin)
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(Staff, StaffAdmin)
admin.site.register(Team, TeamAdmin)
