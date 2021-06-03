from django.contrib import admin

from .models import Post, AssetType, PostPicture

# Register your models here.

class AssetTypeAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
    ]

class PostAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        'desc',
        'location',
        'key',
        'create_at'
    ]

class PostPictureAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'post',
        'picture'
    ]

admin.site.register(Post, PostAdmin)
admin.site.register(AssetType, AssetTypeAdmin)
admin.site.register(PostPicture, PostPictureAdmin)