from django.shortcuts import get_list_or_404, get_object_or_404

# DRF 모듈
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

# 직접 정의한 모듈
from .models import Movie, Review, Comment
from .serializers import MovieSerializer, MovieListSerializer
from .serializers import ReviewSerializer, ReviewListSerializer
from .serializers import CommentSerializer, CommentListSerializer



# Create your views here.
# @api_view(['GET', 'POST'])
# @authentication_classes([JSONWebTokenAuthentication])
# @permission_classes([IsAuthenticated])
# def movies(request):
#     movies = Movie.objects.all()
#     context = {
#         'movies': movies,
#     }
#     return render(request, 'moviedata/movies.html', context)



# 전체영화 정보 제공
@api_view(["GET"])
def movie_list(request):
    if request.method == "GET":
        movies = get_list_or_404(Movie)
        serializer = MovieListSerializer(movies, many=True)
        return Response(serializer.data)




# 단일영화 정보 제공
@api_view(["GET"])
def movie_detail(request, movie_pk):
    if request.method == "GET":
        movie = get_object_or_404(Movie, pk=movie_pk)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)


# 해당 영화 리뷰 리스트 및 리뷰 생성
@api_view(["GET", "POST"])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def review_create_list(request, movie_pk):
    # GET 메서드 -> Review 리스트 보여주기
    if request.method == "GET":
        reviews = Review.objects.all().filter(movie=movie_pk)
        serializer = ReviewListSerializer(reviews, many=True)
        return Response(serializer.data)

    # POST 메서드 -> Review 생성하기
    elif request.method == "POST":
        movie = get_object_or_404(Movie, pk=movie_pk)
        serializer = ReviewListSerializer(data=request.data)

        # 유효성 검사
        if serializer.is_valid(raise_exception=True):
            serializer.save(movie=movie)
            return Response(serializer.data)


# 단일 리뷰 조회,수정,삭제
@api_view(["GET", "PUT", "DELETE"])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def review_detail_update_delete(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.method == "GET":
        serializer = ReviewSerializer(review)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = ReviewSerializer(review, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    elif request.method == "DELETE":
        review.delete()
        return Response(review_pk)


# 해당 리뷰 댓글 리스트 및 댓글 생성
@api_view(["GET", "POST"])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def comment_create_list(request, review_pk):
    if request.method == "GET":
        comments = get_list_or_404(Comment, review=review_pk)
        serializer = CommentListSerializer(comments, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        review = get_object_or_404(Review, pk=review_pk)
        serializer = CommentListSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save(review=review)
            return Response(serializer.data)


# 단일 댓글 조회,수정,삭제
@api_view(["GET", "PUT", "DELETE"])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def comment_detail_update_delete(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.method == "GET":
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    elif request.method == "DELETE":
        comment.delete()
        return Response(comment_pk)
