from django.contrib import admin

from apps.photo_manager.models import Photo


class PhotoAdmin(admin.ModelAdmin):
    pass


admin.site.register(Photo, PhotoAdmin)
