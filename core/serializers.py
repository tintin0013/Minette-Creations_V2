from rest_framework import serializers

from .models import Category, Resource, ResourcePhoto


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


class ResourceSerializer(serializers.ModelSerializer):
    photos = ResourcePhotoSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Resource
        fields = (
            "id",
            "name",
            "description",
            "category",
            "photos",
        )