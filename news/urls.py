from django.conf.urls import include
from django.urls import re_path as url
from django.urls import path
from django.contrib import admin
from .views import NewsSearch
from . import views
from .views import BulkUploadAPIView
urlpatterns = [
    url(r'^$', views.home, name='home'),
    path('upload/', BulkUploadAPIView.as_view(), name='bulk-upload'),
    path('search/', NewsSearch.as_view(), name='news-search'),
    path('category/<int:category_id>/news/', views.news_by_category, name='category_news' ),
    path('news/<int:news_id>/detail/', views.detail_news, name='news-detail'),
    path('scraping/', views.scraping, name="scraping"),
    ]