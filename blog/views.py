from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post

# Create your views here.

class PostList(ListView):
  model = Post
  # post_list.html : class이름_list.html 내부적으로 정의가 되어있기 때문에 생략가능
  # 파일명을 위에 있는 규칙으로 하지 않을 경우 명시해줘야함. 
  # template_name = 'blog/post_list.html'

class PostDetail(DetailView):
  model = Post
  # template_name = 'blog/post_detail.html'
