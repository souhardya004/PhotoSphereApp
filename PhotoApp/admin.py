from django.contrib import admin

from PhotoApp.models import Photo, Photo_category

# Register your models here.
class PhotoInline(admin.TabularInline):
    model = Photo_category
    extra = 1
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'date', 'image', 'uploaded_at')
    inlines = [PhotoInline]
class Photo_categoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'category_types')



admin.site.register(Photo_category, Photo_categoryAdmin)
admin.site.register(Photo, PhotoAdmin)