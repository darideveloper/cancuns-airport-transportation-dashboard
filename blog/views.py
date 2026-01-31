from rest_framework import viewsets

from blog import serializers
from blog import models


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    """ Api viewset for Post model """
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostListItemSerializer
    lookup_field = "slug"

    def get_queryset(self):
        """ filter with get parameters """
        queryset = models.Post.objects.all().order_by("-updated_at")

        # Get lang rrom headers Accept-Language
        lang = self.request.META.get("HTTP_ACCEPT_LANGUAGE", None)

        # Filter by lang
        if lang is not None:
            queryset = queryset.filter(lang=lang)

        # return queryset
        return queryset
    
    def get_serializer_class(self, *args, **kwargs):
        """ Return serializer class """
        if "details" in self.request.query_params:
            return serializers.PostDetailSerializer
        if "summary" in self.request.query_params:
            return serializers.PostListItemSerializer
        return self.serializer_class