from rest_framework import serializers
from blog import models


class PostListItemSerializer(serializers.ModelSerializer):
    """ Api serializer for Post model """
    
    class Meta:
        model = models.Post
        fields = (
            "id",
            "title",
            "slug",
            "lang",
            "banner_image_url",
            "description",
            "author",
            "created_at",
            "updated_at",
        )
        
        
class PostDetailSerializer(PostListItemSerializer):
    """ Api serializer for Post model """
    
    related_post = serializers.SerializerMethodField()
    
    class Meta:
        model = models.Post
        fields = "__all__"
        
    def get_related_post(self, obj) -> dict:
        """Retrieve related post as dict"""
        
        if not obj.related_post:
            return None
        
        return obj.related_post.slug