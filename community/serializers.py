# from django.db.models import fields
from rest_framework import serializers
from .models import Community, CommunityComment
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username',]

class CommunityListSerializer(serializers.ModelSerializer):
  class Meta:
    model = Community
    fields = "__all__"


class CommunityCommentListSerializer(serializers.ModelSerializer):
  class Meta:
    model = CommunityComment
    fields = "__all__"
    read_only_fields = [
        "community",
    ]

class CommunityCommentSerializer(serializers.ModelSerializer):
  class Meta:
    model = CommunityComment
    fields = "__all__"
    read_only_fields = [
        "community",
    ]

class CommunitySerializer(serializers.ModelSerializer):
    comment_set = CommunityCommentSerializer(many=True, read_only=True)
    comment_count = serializers.IntegerField(source="comment_set.count", read_only=True)
    
    class Meta:
        model = Community
        fields = "__all__"
        read_only_fields = [
          "user",
          "comment_set",
          "comment_count",
        ]