from django.db import models
from django.contrib.auth import get_user_model

MARK_CHOICES=[
    (1, 'LIKE'),
    (0, 'DISLIKE')
]
User = get_user_model()


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    image = models.ImageField(upload_to='images/')
    created_at = models.DateTimeField(auto_now_add=True)


# для доп. задания
# class PostImage(models.Model):
#     ...


class Like(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    mark = models.PositiveSmallIntegerField(choices=MARK_CHOICES)

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)