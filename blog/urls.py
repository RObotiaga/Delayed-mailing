from django.urls import path
from . import views
from django.views.decorators.cache import cache_page

app_name = 'blog'
urlpatterns = [
    path('main/', views.MainPageView.as_view(), name='main_page'),
    path('', cache_page(60)(views.PostListView.as_view()), name='post_list'),
    path('post/<slug:slug>/', cache_page(60)(views.PostDetailView.as_view()), name='post_detail'),
    path('new_post/', cache_page(60)(views.PostCreateView.as_view()), name='create_post'),
    path('post/<slug:slug>/edit/', views.PostEditView.as_view(), name='edit_post'),
    path('post/<slug:slug>/delete/', views.PostDeleteView.as_view(), name='delete_post'),
]
