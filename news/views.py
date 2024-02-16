from django.shortcuts import redirect, render
from datetime import datetime
from .models import Category, Tag
from django.db.models import Q
from django.views import View
from .script import main


# Create your views here.
def home(request):
    datatimenow = datetime.now()
    all_news = News.objects.all().order_by('-id')[:5]
    random_news = News.objects.order_by('?')[:5]
    one_category = News.objects.filter(category=1)
    two_category = News.objects.filter(category=2)
    three_category = News.objects.filter(category=3)
    tranding_cats = Category.objects.filter(tranding=True)
    tags = Tag.objects.all()
    context = {
        'datatimenow': datatimenow,
        'random_news': random_news,
        'one_category': one_category,
        'two_category': two_category,
        'three_category': three_category,
        'tranding_cats':tranding_cats,
        'all_news':all_news,
        'tags':tags
    }
    return render(request, 'index.html', context)

def for_all_pages(request):
    ten_news = News.objects.all().order_by('-id')[:10]
    category = Category.objects.filter(tranding=True)
    return {
        'ten_news': ten_news,
        'category': category,
    }
    
def scraping(request):
    if request.user.is_authenticated:
        main()
    return redirect(home)
        
# SECTION GET CATEGORY'S NEWS
def news_by_category(request, category_id):
    category_id = Category.objects.get(pk=category_id)
    category_news = News.objects.filter(category=category_id)
    return render(request, 'post_pages/category.html', {'category_id': category_id, 'category_news': category_news})
    
# SECTION NEWS DETAIL
def detail_news(request, news_id):    
    news_id = News.objects.get(pk=news_id)
    random_news = News.objects.order_by('?')[:5]
    return render(request, 'post_pages/single.html', {'news_id': news_id, 'random_news':random_news})

    
class NewsSearch(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('query')
        
        news_list = News.objects.filter(
            Q(title__icontains=query) if query else News.objects.all()
        )
        
        context = {
            'news_list': news_list,
        }
        
        return render(request, 'search.html', context)

# views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import DjangoModelPermissions
from .api import NewsSerializer
from .models import News
import json

class BulkUploadAPIView(APIView):
    permission_classes = [DjangoModelPermissions]
    queryset = News.objects.all()  # Установите ваш queryset

    def post(self, request):
        data = request.data
        serializer = NewsSerializer(data=data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
