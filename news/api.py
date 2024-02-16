from .models import News, Category, Tag
from rest_framework import serializers, viewsets


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        slug = serializers.SlugField(read_only=True, source='title')
        fields = '__all__'
        
        

class NewsSerializer(serializers.ModelSerializer):
    image = serializers.CharField()
    category_id = serializers.IntegerField()
    slug = serializers.SlugField(read_only=True, source='title')
    class Meta:
        model = News
        fields = ['title', 'image', 'detail','slug', 'category_id','add_time', 'post_viewcount', 'tags','seo_keywords', 'seo_description']

# ViewSets define the view behavior.
class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer