from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


class LikeAdmin(admin.ModelAdmin):
    list_display = ['user_from', 'user_to']


class ProfilePhotoInline(admin.StackedInline):
    model = ProfilePhoto
    extra = 1


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'nickname', 'firstname', 'lastname', 'location', 'description', 'type', 'get_image']
    inlines = [ProfilePhotoInline]
    # readonly_fields = ('get_image',)

    def get_image(self, obj):
        if obj.main_photo:
            return mark_safe(f'<img src={obj.main_photo.url} width="100" height="120"')


    get_image.short_description = "Фото"


class ProfilePhotoAdmin(admin.ModelAdmin):
    list_display = ['profile', 'date_pub', 'get_image']
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100" height="120"')

    get_image.short_description = "Фото"


admin.site.register(Profile, ProfileAdmin)
admin.site.register(ProfilePhoto, ProfilePhotoAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(UnLike)
admin.site.register(Reciprocity)
admin.site.register(Chat)
admin.site.register(Message)