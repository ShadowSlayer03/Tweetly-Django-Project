
from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.index,name="index"),
    path('create/',views.tweet_submit,name="tweet_submit"),
    path('<int:tweet_id>/edit/', views.tweet_edit,name="tweet_edit"),
    path('<int:tweet_id>/delete/', views.tweet_delete,name="tweet_delete"),
] 
