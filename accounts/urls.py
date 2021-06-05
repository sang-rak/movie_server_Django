from rest_framework_jwt.views import obtain_jwt_token

from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup),
    path('userinfo/', views.userinfo),
    path('login/', obtain_jwt_token),
] 