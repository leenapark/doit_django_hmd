from django.shortcuts import render, redirect
from django.utils.text import slugify
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Post, Category, Tag, Comment
from .form import PostForm, CommentForm

# Create your views here.
# 게시글 목록
class PostList(ListView):
  model = Post
  # post_list.html : class이름_list.html 내부적으로 정의가 되어있기 때문에 생략가능
  # 파일명을 위에 있는 규칙으로 하지 않을 경우 명시해줘야함. 
  # template_name = 'blog/post_list.html'
  ordering = "-pk"
  # 한 페이지 당 보여줄 포스트 갯수 정하기
  paginate_by = 4

  def get_context_data(self, **kwargs):
    context = super(PostList, self).get_context_data()
    context["categories"] = Category.objects.all()
    context["no_category_post_count"] = Post.objects.filter(category = None).count()
    return context

# 게시글 읽기
class PostDetail(DetailView):
  model = Post
  # template_name = 'blog/post_detail.html'
  
  def get_context_data(self, **kwargs):
    context = super(PostDetail, self).get_context_data()
    context["categories"] = Category.objects.all()
    context["no_category_post_count"] = Post.objects.filter(category = None).count()
    context["comment_form"] = CommentForm
    return context

# 게시글 쓰기
class PostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
  # model = Post
  # fields = ["title", "hook_text", "content", "head_image", "file_upload", "category"]
  form_class = PostForm
  template_name = "blog/post_form.html"

  def test_func(self):
    return self.request.user.is_superuser or self.request.user.is_staff

  def form_valid(self, form):
    current_user = self.request.user
    if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
      form.instance.author = current_user
      response = super(PostCreate, self).form_valid(form)
      tags_str = self.request.POST.get("tags_str")
      print(tags_str)

      if tags_str:
        tags_str = tags_str.strip()
        tags_str = tags_str.replace(",", ";")
        tags_list = tags_str.split(";")


        for t in tags_list:
          t = t.strip()
          tag, is_tag_created = Tag.objects.get_or_create(name=t)
          if is_tag_created:
            tag.slug = slugify(t, allow_unicode=True)
            tag.save()
          self.object.tags.add(tag)

      return response
    else:
      return redirect("/blog/")
    
# 포스트 수정
class PostUpdate(LoginRequiredMixin, UpdateView):
  model = Post
  # fields = ["title", "hook_text", "content", "head_image", "file_upload", "category", "tags"]

  form_class = PostForm
  template_name = "blog/post_update_form.html"

  def get_context_data(self, **kwargs):
    context = super().get_context_data()
    if self.object.tags.exists():
      tags_str_list = list()
      for t in self.object.tags.all():
        tags_str_list.append(t.name)
      context["tags_str_default"] = "; ".join(tags_str_list)
    return context

  def form_valid(self, form):
    response = super(PostUpdate, self).form_valid(form)
    self.object.tags.clear()
    tags_str = self.request.POST.get("tags_str")
    if tags_str:
        tags_str = tags_str.strip()
        tags_str = tags_str.replace(",", ";")
        tags_list = tags_str.split(";")
        for t in tags_list:
          t = t.strip()
          tag, is_tag_created = Tag.objects.get_or_create(name=t)
          if is_tag_created:
            tag.slug = slugify(t, allow_unicode=True)
            tag.save()
          self.object.tags.add(tag)

    return response

  def dispatch(self, request, *args, **kwargs):
    if request.user.is_authenticated and request.user == self.get_object().author:
      return super(PostUpdate, self).dispatch(request, *args, **kwargs)
    else:
      raise PermissionDenied

# 게시글 검색
class PostSearch(PostList):
  paginate_by = None
  
  def get_queryset(self):
    q = self.kwargs["q"]
    post_list = Post.objects.filter(
      Q(title__contains=q) | Q(tags__name__contains=q) | Q(content__contains=q)
    ).distinct()
    return post_list
  
  def get_context_data(self, **kwargs):
    context = super(PostSearch, self).get_context_data()
    q = self.kwargs["q"]
    context["search_info"] = f"Search: {q} ({self.get_queryset().count()})"
    return context

""" *************댓글********************* """

def new_comment(request, pk):
  if request.user.is_authenticated:
    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
      comment_form = CommentForm(request.POST)
      if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
        return redirect(comment.get_absolute_url())
      else:
        return redirect(post.get_absolute_url())
    else:
      raise PermissionDenied

# 댓글 수정
class CommentUpdate(LoginRequiredMixin, UpdateView):
  model = Comment
  form_class = CommentForm
  def dispatch(self, request, *args, **kwargs):
    if request.user.is_authenticated and request.user == self.get_object().author:
      return super(CommentUpdate, self).dispatch(request, *args, **kwargs)
    else:
      raise PermissionDenied

# 댓글 삭제
def delete_comment(request, pk):
  comment = get_object_or_404(Comment, pk=pk)
  post = comment.post
  if request.user.is_authenticated and request.user == comment.author:
    comment.delete()
    return redirect(post.get_absolute_url())
  else:
    raise PermissionDenied

""" *************카테고리********************* """
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


""" *****************태그***************** """
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


