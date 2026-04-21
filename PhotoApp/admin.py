from django.contrib import admin

from PhotoApp.models import Photo, Photo_category,Like,Comment

# Register your models here.
class PhotoInline(admin.TabularInline):
    model = Photo_category
    extra = 1
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'date', 'image', 'uploaded_at')
    inlines = [PhotoInline]
class Photo_categoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'category_types')
class likeAdmin(admin.ModelAdmin) :
    list_display = ('photo','like')
class commentAdmin(admin.ModelAdmin) :
    list_display = ('photo','comment')



admin.site.register(Photo_category, Photo_categoryAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Like,likeAdmin)
admin.site.register(Comment,commentAdmin)