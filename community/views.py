import re
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .serializers import CommunitySerializer, CommunityListSerializer, CommunityCommentListSerializer, CommunityCommentSerializer
from .models import Community, CommunityComment


@api_view(["GET"])
def community_list(request):
    if request.method == "GET":
        communities = get_list_or_404(Community)
        serializer = CommunityListSerializer(communities, many=True)
        return Response(serializer.data)


@api_view(["GET"])
def community_detail(request, community_pk):
    if request.method == "GET":
        community = get_object_or_404(Community, pk=community_pk)
        serializer = CommunitySerializer(community)
        return Response(serializer.data)


@api_view(['GET', 'POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def community_create(request):
    if request.method == 'GET':
        communities = request.user.community_set.all()
        serializer = CommunityListSerializer(communities, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CommunitySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['PUT', 'DELETE'])
def community_update_delete(request, community_pk):
    community = get_object_or_404(Community, pk=community_pk)
    if request.method == 'PUT':
        serializer = CommunitySerializer(community, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    elif request.method == 'DELETE':
        community.delete()
        return Response({ 'id': community_pk })



@api_view(["GET", "POST"])
def comment_create_list(request, community_pk):
    if request.method == "GET":
        comments = get_list_or_404(CommunityComment) #, review=community_pk
        serializer = CommunityCommentListSerializer(comments, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        community = get_object_or_404(Community, pk=community_pk)
        serializer = CommunityCommentSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save(community=community)
            return Response(serializer.data)



@api_view(["GET", "PUT", "DELETE"])
def comment_detail_update_delete(request, comment_pk):
    comment = get_object_or_404(CommunityComment, pk=comment_pk)
    if request.method == "GET":
        serializer = CommunityCommentListSerializer(comment)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = CommunityCommentSerializer(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    elif request.method == "DELETE":
        comment.delete()
        return Response(comment_pk)
