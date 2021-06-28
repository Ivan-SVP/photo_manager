import logging

from rest_framework import viewsets, serializers, permissions
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.photo_manager.models import Photo

logger = logging.getLogger(__name__)


class PhotoPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return getattr(request.user, 'can_upload', False)


class PhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Photo
        fields = ['id', 'photo', 'comment', 'created']

    def validate_photo(self, value):
        if hash(value) % 2:
            raise serializers.ValidationError("Not valid photo")
        return value


class PartialUpdatePhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Photo
        fields = ['comment']


class PhotoViewSet(viewsets.ModelViewSet):
    """CRUD для работы пользователя со своими фотографиями."""
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = [PhotoPermission, IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        if not kwargs.get('partial', False):
            raise MethodNotAllowed("PUT", detail="Use PATCH for partial update.")
        return super().update(request, *args, **kwargs)

    @action(detail=False, methods=['get'])
    def archive(self, request, *args, **kwargs):
        """Удаленные фотографии"""
        queryset = Photo.deleted_objects.filter(user=request.user)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action == 'update':
            return PartialUpdatePhotoSerializer
        return self.serializer_class

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
