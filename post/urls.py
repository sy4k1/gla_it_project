from django.urls import path

from . import views

urlpatterns = [
    path('query', views.query, name='query'),
    path('publish', views.publish, name='publish'),
    path('query_comments', views.query_comments, name='query_comments'),
    path('query_like_status', views.query_like_status, name='query_like_status'),
    path('like', views.like, name='like'),
    path('comment', views.comment, name='comment'),
    path('delete', views.delete, name='delete'),
]