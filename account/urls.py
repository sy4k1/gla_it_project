from django.urls import path

from . import views

urlpatterns = [
    path('query', views.query, name='query'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('signup', views.signup, name='signup'),
    path('send_passcode', views.send_passcode, name='send_passcode'),
    path('query_follow_status', views.query_follow_status, name='query_follow_status'),
    path('follow', views.follow, name='follow'),
    path('query_notification', views.query_notification, name='query_notification'),
    path('read_notification', views.read_notification, name='read_notification'),

]