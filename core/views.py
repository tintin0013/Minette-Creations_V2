from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from .models import Category, Resource, Reservation, UserProfile
from .serializers import (
    CategorySerializer,
    ResourceSerializer,
    ReservationSerializer,
)


# =======================
# CATEGORIES
# =======================

class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.filter(is_active=True, parent__isnull=True)
    serializer_class = CategorySerializer


# =======================
# RESOURCES
# =======================

class ResourceListAPIView(generics.ListAPIView):
    serializer_class = ResourceSerializer

    def get_queryset(self):
        queryset = Resource.objects.filter(is_active=True)

        category_slug = self.request.query_params.get("category")

        if category_slug:
            queryset = queryset.filter(
                category__slug=category_slug,
                category__is_active=True
            )

        return queryset


class ResourceDetailAPIView(generics.RetrieveAPIView):
    queryset = Resource.objects.filter(is_active=True)
    serializer_class = ResourceSerializer


# =======================
# RESERVATION CREATE
# =======================

class ReservationCreateAPIView(generics.CreateAPIView):
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        clerk_user_id = self.request.user.id

        # Création automatique du profil si inexistant
        UserProfile.objects.get_or_create(
            clerk_user_id=clerk_user_id
        )

        serializer.save(user_clerk_id=clerk_user_id)

    def get_serializer_context(self):
        return {"request": self.request}


# =======================
# USER RESERVATIONS LIST
# =======================

class UserReservationListAPIView(generics.ListAPIView):
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Reservation.objects.filter(
            user_clerk_id=self.request.user.id
        )


# =======================
# ADMIN RESERVATIONS LIST
# =======================

class AdminReservationListAPIView(generics.ListAPIView):
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        profile, created = UserProfile.objects.get_or_create(
            clerk_user_id=self.request.user.id
        )

        if not profile.is_admin:
            raise PermissionDenied("Admin access required.")

        return Reservation.objects.all()


# =======================
# TEST PROTECTED
# =======================

class ProtectedAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile, created = UserProfile.objects.get_or_create(
            clerk_user_id=request.user.id
        )

        return Response({
            "message": "Access granted",
            "clerk_user_id": request.user.id,
            "is_admin": profile.is_admin
        })