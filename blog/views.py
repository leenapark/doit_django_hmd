from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView
from .models import Post, Category, Tag

# Create your views here.

class PostList(ListView):
  model = Post
  # post_list.html : class이름_list.html 내부적으로 정의가 되어있기 때문에 생략가능
  # 파일명을 위에 있는 규칙으로 하지 않을 경우 명시해줘야함. 
  # template_name = 'blog/post_list.html'
  ordering = "-pk"

  def get_context_data(self, **kwargs):
    context = super(PostList, self).get_context_data()
    context["categories"] = Category.objects.all()
    context["no_category_post_count"] = Post.objects.filter(category = None).count()
    return context

class PostDetail(DetailView):
  model = Post
  # template_name = 'blog/post_detail.html'
  
  def get_context_data(self, **kwargs):
    context = super(PostDetail, self).get_context_data()
    context["categories"] = Category.objects.all()
    context["no_category_post_count"] = Post.objects.filter(category = None).count()
    return context
    
class PostCreate(LoginRequiredMixin, CreateView):
  model = Post
  fields = ["title", "hook_text", "content", "head_image", "file_upload", "category"]

  def form_valid(self, form):
    current_user = self.request.user
    if current_user.is_authenticated:
      form.instance.author = current_user
      return super(PostCreate, self).form_valid(form)
    else:
      return redirect("/blog/")
  
def category_page(request, slug):
  # context = {}
  # category = Category.objects.get(slug=slug)
  # context["post_list"] = Post.objects.filter(category=category)
  # context["categories"] = Category.objects.all()
  # context["no_category_post_count"] = Post.objects.filter(category = None).count()
  # context["category"] = category
  # print(context)

  # return render(
  #   request,
  #   "blog/post_list.html",
  #   context
  # )
  if slug == "no_category":
    category = "미분류"
    post_list = Post.objects.filter(category=None)
  else:
    category = Category.objects.get(slug=slug)
    post_list = Post.objects.filter(category=category)

  return render(
    request,
    "blog/post_list.html",
    {
      "post_list": post_list,
      "categories": Category.objects.all(),
      "no_category_post_count": Post.objects.filter(category=None).count(),
      "category": category
    }
  )

def tag_page(request, slug):
  tagcontext = {}
  tag = Tag.objects.get(slug=slug)
  post_list = tag.post_set.all()
  tagcontext["post_list"] = post_list
  tagcontext["tag"] = tag
  tagcontext["categories"] = Category.objects.all()
  tagcontext["no_category_post_count"] = Post.objects.filter(category=None).count()


  return render(
    request,
    "blog/post_list.html",
    tagcontext
  )