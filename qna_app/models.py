from django.db import models

# 요청사항
from lyl_b import settings


class Post(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField()

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    post_id = models.ForeignKey(
        Post,
        related_name='post_comment',
        on_delete=models.CASCADE,
        db_column='post_id'
    )

    comment = models.TextField()

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)