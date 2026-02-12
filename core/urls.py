from django.urls import path

from .views import (
    CategoryListAPIView,
    ResourceListAPIView,
    ResourceDetailAPIView,
    ProtectedAPIView,
)

urlpatterns = [
    path("categories/", CategoryListAPIView.as_view(), name="category-list"),
    path("resources/", ResourceListAPIView.as_view(), name="resource-list"),
    path("resources/<int:pk>/", ResourceDetailAPIView.as_view(), name="resource-detail"),
    path("protected/", ProtectedAPIView.as_view(), name="protected"),
]