from django.urls import path
from . import views

urlpatterns = [
    # 영화 리스트 전체
    path("", views.movie_list),
    # 단일 영화 상세 정보
    path("<int:movie_pk>/", views.movie_detail),
    # 리뷰 리스트, 생성
    path("<int:movie_pk>/review/", views.review_create_list),
    # 리뷰 단일, 수정, 삭제
    path("review/<int:review_pk>/", views.review_detail_update_delete),
    # 댓글 리스트, 생성
    path("<int:review_pk>/comment/", views.comment_create_list),
    # 댓글 단일, 수정, 삭제
    path("comment/<int:comment_pk>/", views.comment_detail_update_delete),
]
