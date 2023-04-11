from django.urls import path
from . import views

urlpatterns = [
    # /blog/
    path('', views.PostList.as_view(), name='post_list'),
    path('<int:pk>/', views.PostDetail.as_view(), name='post_etail'),
    path("category/<str:slug>/", views.category_page),
    path("tag/<str:slug>/", views.tag_page),
    path("create_post/", views.PostCreate.as_view(), name="writeform"),
    path("update_post/<int:pk>/", views.PostUpdate.as_view()),
    path("search/<str:q>/", views.PostSearch.as_view()),
    path("<int:pk>/new_comment/", views.new_comment),
    # 댓글 수정
    path("update_comment/<int:pk>/", views.CommentUpdate.as_view()),
    # 댓글 삭제
    path("delete_comment/<int:pk>", views.delete_comment),
]