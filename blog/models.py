from django.db import models
from django.contrib.auth.models import User
import os

# Create your models here.

# category
class Category(models.Model):
  name = models.CharField(max_length=50, unique=True)
  slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

  def __str__(self):
    return self.name
  
  class Meta:
    verbose_name_plural = "Categories"
  
  def get_absolute_url(self):
    return f'/blog/category/{self.slug}/'

# tag
class Tag(models.Model):
  name = models.CharField(max_length=50)
  slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

  def __str__(self):
    return self.name
  
  def get_absolute_url(self):
    return f'/blog/tag/{self.slug}/'  
  

# post
class Post(models.Model):
  title = models.CharField(max_length=30)
  hook_text = models.CharField(max_length=100, blank=True)
  content = models.TextField()

  head_image = models.ImageField(upload_to="blog/images/%Y/%m/%d/", blank=True)
  file_upload = models.FileField(upload_to="blog/files/%Y/%m/%d/", blank=True)

  created_at = models.DateField(auto_now_add=True)
  updated_at = models.DateField(auto_now=True)

  # User
  # author = models.ForeignKey(User, on_delete=models.CASCADE) User 삭제 시 포스트도 삭제 된다
  author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

  # Category
  category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)

  # Tags
  tags = models.ManyToManyField(Tag, blank=True)

  def __str__(self):
    return f'[{self.pk}] {self.title} :: {self.author}'
  
  def get_absolute_url(self):
    return f'/blog/{self.pk}/'
  
  def get_file_name(self):
    return os.path.basename(self.file_upload.name)
  
  def get_file_ext(self):
    return self.get_file_name().split(".")[-1]

# comment
# 댓글이 달리는 포스트
# 댓글 작성자 정보/시간
# 댓글 작성 공간
class Comment(models.Model):
  post = models.ForeignKey(Post, on_delete=models.CASCADE)
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  content = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  modified_at = models.DateTimeField(auto_now=True)


  def __str__(self):
    return f"{self.author}::{self.content}"

  def get_absolute_url(self):
    return f'{self.post.get_absolute_url()}#comment-{self.pk}'
  
  # user profile img
  def get_avatar_url(self):
    if self.author.socialaccount_set.exists():
      self.author.socialaccount_set.first().get_avatar_url()
    else:
      return "http://placehold.it/50x50"