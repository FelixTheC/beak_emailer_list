from django.contrib import admin

from kita_friends.models import KitaFriends


@admin.register(KitaFriends)
class KitaFriendsAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'kita')
