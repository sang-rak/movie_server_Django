from django.urls import path
from . import views


urlpatterns = [
    path('', views.community_list),
    path("community_c/", views.community_create),
    path("<int:community_pk>/", views.community_detail),
    path("community_d_u/<int:community_pk>/", views.community_update_delete),

    path("int:community_pk>/comments/", views.comment_create_list),
    path("comment/<int:comment_pk>/", views.comment_detail_update_delete),
]
