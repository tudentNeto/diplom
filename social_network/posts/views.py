from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics, status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from posts.models import Post, Like, Comment
from posts.serializers import PostSerializer, LikeSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticated
from posts.permissions import IsOwner
from django.shortcuts import get_object_or_404



class PostListCreateAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]


class PostDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsOwner]


class CommentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    lookup_url_kwarg ='pk'
    def get(self, request, pk):
        queryset = Comment.objects.filter(post_id=pk)
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        id_post=self.kwargs.get(self.lookup_url_kwarg)
        post = get_object_or_404(Post, id=id_post)
        serializer.save(author=self.request.user, post_id=id_post)


class CommentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsOwner]



class LikeAPIView(generics.CreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = 'pk'
    def perform_create(self, serializer):
        id_post = self.kwargs.get(self.lookup_url_kwarg)
        post = get_object_or_404(Post, id=id_post)
        queryset = Like.objects.filter(author=self.request.user, post_id=id_post)
        if queryset.exists():
            raise serializers.ValidationError('You have already liked this post!')
        else:
            serializer.save(author=self.request.user, post_id=id_post)
