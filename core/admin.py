from django.contrib import admin

from .models import (
    UserProfile,
    Category,
    Resource,
    ResourcePhoto,
    ResourceOption,
    ResourceOptionValue,
    Reservation,  # 🔥 AJOUTÉ
)


# =========================
# USER PROFILE ADMIN
# =========================

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("email", "clerk_user_id", "is_admin", "created_at")
    list_filter = ("is_admin",)
    search_fields = ("email", "clerk_user_id")
    ordering = ("-created_at",)


# =========================
# CATEGORY
# =========================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "parent", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("parent__name", "name")


# =========================
# RESOURCE OPTION VALUES INLINE
# =========================

class ResourceOptionValueInline(admin.TabularInline):
    model = ResourceOptionValue
    extra = 1


# =========================
# RESOURCE OPTION INLINE
# =========================

class ResourceOptionInline(admin.StackedInline):
    model = ResourceOption
    extra = 1
    show_change_link = True


# =========================
# RESOURCE PHOTO INLINE
# =========================

class ResourcePhotoInline(admin.TabularInline):
    model = ResourcePhoto
    extra = 1
    ordering = ("position",)


# =========================
# RESOURCE ADMIN
# =========================

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "is_active", "created_at")
    list_filter = ("is_active", "category")
    search_fields = ("name", "description")
    inlines = [
        ResourcePhotoInline,
        ResourceOptionInline,
    ]


# =========================
# RESOURCE OPTION ADMIN
# =========================

@admin.register(ResourceOption)
class ResourceOptionAdmin(admin.ModelAdmin):
    list_display = ("name", "resource", "created_at")
    list_filter = ("resource",)
    inlines = [ResourceOptionValueInline]


# =========================
# RESOURCE PHOTO ADMIN
# =========================

@admin.register(ResourcePhoto)
class ResourcePhotoAdmin(admin.ModelAdmin):
    list_display = ("id", "resource", "position", "created_at")
    list_filter = ("resource",)
    ordering = ("resource", "position")


# =========================
# RESOURCE OPTION VALUE ADMIN
# =========================

@admin.register(ResourceOptionValue)
class ResourceOptionValueAdmin(admin.ModelAdmin):
    list_display = ("value", "option", "created_at")
    list_filter = ("option",)


# =========================
# 🔥 RESERVATION ADMIN
# =========================

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("id", "resource", "user_clerk_id", "status", "created_at")
    list_filter = ("status", "resource")
    search_fields = ("user_clerk_id",)
    ordering = ("-created_at",)