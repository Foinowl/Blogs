from django.urls import path
from .views import (
    PostListView,
    TagListView,
    tags_detail,
    TagDetailView,
    TagCreateView,
    TagUpdateView,
    PostDetailView,
    PostCreateView,
    TagDeleteView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    SearchResultsView
)
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('tag/', TagListView.as_view(), name='tag-home'),
    path('tags/<str:slug>', tags_detail, name='tags-detail_url'),
    path('tag/<int:pk>/', TagDetailView.as_view(), name='tag-detail'),
    path('tag/new', TagCreateView.as_view(), name='tag-new'),
    path('tag/<int:pk>/update/', TagUpdateView.as_view(), name='tag-update'),
    path('tag/<int:pk>/delete/', TagDeleteView.as_view(), name='tag-delete'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('search/', SearchResultsView.as_view(), name='search-results'),
    path('about/', views.about, name='blog-about'),
]