from django.contrib import admin

from .models import Category, Resource, ResourcePhoto


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "parent", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("parent__name", "name")


class ResourcePhotoInline(admin.TabularInline):
    model = ResourcePhoto
    extra = 1
    ordering = ("position",)


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "is_active", "created_at")
    list_filter = ("is_active", "category")
    search_fields = ("name", "description")
    inlines = [ResourcePhotoInline]


@admin.register(ResourcePhoto)
class ResourcePhotoAdmin(admin.ModelAdmin):
    list_display = ("id", "resource", "position", "created_at")
    list_filter = ("resource",)
    ordering = ("resource", "position")