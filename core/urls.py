from django.urls import path

from .views import (
    CategoryListAPIView,
    ResourceListAPIView,
    ResourceDetailAPIView,
    ProtectedAPIView,
    ReservationCreateAPIView,
    UserReservationListAPIView,
    AdminReservationListAPIView,  # 🔥 AJOUTÉ
)

urlpatterns = [
    path("categories/", CategoryListAPIView.as_view(), name="category-list"),
    path("resources/", ResourceListAPIView.as_view(), name="resource-list"),
    path("resources/<int:pk>/", ResourceDetailAPIView.as_view(), name="resource-detail"),

    # 🔐 Test
    path("protected/", ProtectedAPIView.as_view(), name="protected"),

    # 📦 Reservation
    path("reservations/", ReservationCreateAPIView.as_view(), name="reservation-create"),

    # 👤 Mes réservations
    path("my-reservations/", UserReservationListAPIView.as_view(), name="my-reservations"),

    # 🛠️ Admin - toutes les réservations
    path("admin-reservations/", AdminReservationListAPIView.as_view(), name="admin-reservations"),
]