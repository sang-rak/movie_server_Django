from rest_framework import serializers
from .models import Movie, Review, Comment

class MovieListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = "__all__"


class ReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"
        read_only_fields = [
            "movie",
        ]


class CommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = [
            "review",
        ]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = [
            "review",
        ]


class ReviewSerializer(serializers.ModelSerializer):
    comment_set = CommentSerializer(many=True, read_only=True)
    comment_count = serializers.IntegerField(source="comment_set.count", read_only=True)

    class Meta:
        model = Review
        fields = "__all__"
        read_only_fields = [
            "movie",
            "comment_set",
            "comment_count",
        ]


class MovieSerializer(serializers.ModelSerializer):
    review_set = ReviewSerializer(many=True, read_only=True)
    review_count = serializers.IntegerField(source="review_set.count", read_only=True)

    class Meta:
        model = Movie
        fields = "__all__"
        read_only_fields = [
            "review_set",
            "review_count",
        ]