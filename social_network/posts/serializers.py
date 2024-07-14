from rest_framework import serializers

from posts.models import Comment, Post, Like



class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['author', 'text', 'created_at']
        read_only_fields=['author',]


        def create(self, validated_data):
            print(validated_data['author'])
            return Comment.objects.create(**validated_data)



class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ['author', 'text', 'image', 'created_at', 'comments', 'likes_count']
        read_only_fields=['author',]


    def get_likes_count(self, obj):
        queryset = Like.objects.filter(post=obj)
        return queryset.count()



class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'author', 'post_id', 'mark']
        read_only_fields = ['author', 'post_id']
