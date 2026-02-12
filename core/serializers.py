from rest_framework import serializers

from .models import (
    Category,
    Resource,
    ResourcePhoto,
    ResourceOption,
    ResourceOptionValue,
    Reservation,
    UserProfile,
)


# =======================
# CATEGORY
# =======================

class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "slug",
            "parent",
            "children",
        )

    def get_children(self, obj):
        children = obj.children.filter(is_active=True)
        return CategorySerializer(children, many=True).data


# =======================
# PHOTOS
# =======================

class ResourcePhotoSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ResourcePhoto
        fields = (
            "id",
            "image_url",
            "position",
        )

    def get_image_url(self, obj):
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url


# =======================
# OPTIONS
# =======================

class ResourceOptionValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceOptionValue
        fields = (
            "id",
            "value",
        )


class ResourceOptionSerializer(serializers.ModelSerializer):
    values = ResourceOptionValueSerializer(many=True, read_only=True)

    class Meta:
        model = ResourceOption
        fields = (
            "id",
            "name",
            "values",
        )


# =======================
# RESOURCE
# =======================

class ResourceSerializer(serializers.ModelSerializer):
    photos = ResourcePhotoSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    options = ResourceOptionSerializer(many=True, read_only=True)

    class Meta:
        model = Resource
        fields = (
            "id",
            "name",
            "description",
            "category",
            "photos",
            "options",
        )


# =======================
# RESERVATION
# =======================

class ReservationSerializer(serializers.ModelSerializer):
    selected_options = serializers.PrimaryKeyRelatedField(
        queryset=ResourceOptionValue.objects.all(),
        many=True,
        required=False
    )

    # 🔥 Infos lisibles pour admin
    resource_name = serializers.CharField(source="resource.name", read_only=True)
    user_email = serializers.SerializerMethodField()
    user_first_name = serializers.SerializerMethodField()
    user_last_name = serializers.SerializerMethodField()
    user_clerk_id = serializers.CharField(read_only=True)

    class Meta:
        model = Reservation
        fields = (
            "id",
            "resource",
            "resource_name",
            "user_clerk_id",
            "user_email",
            "user_first_name",
            "user_last_name",
            "selected_options",
            "status",
            "created_at",
        )
        read_only_fields = (
            "status",
            "created_at",
            "user_clerk_id",
        )

    def get_user_profile(self, obj):
        return UserProfile.objects.filter(
            clerk_user_id=obj.user_clerk_id
        ).first()

    def get_user_email(self, obj):
        profile = self.get_user_profile(obj)
        return profile.email if profile else None

    def get_user_first_name(self, obj):
        profile = self.get_user_profile(obj)
        return profile.first_name if profile else None

    def get_user_last_name(self, obj):
        profile = self.get_user_profile(obj)
        return profile.last_name if profile else None

    def create(self, validated_data):
        request = self.context["request"]
        selected_options = validated_data.pop("selected_options", [])

        reservation = Reservation.objects.create(
            user_clerk_id=request.user.id,
            **validated_data
        )

        reservation.selected_options.set(selected_options)

        return reservation