from rest_framework import serializers
from .models import BlogPost, BlogCategory, Newsletter, ContactMessage

class BlogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = ['id', 'name', 'slug', 'description']
        read_only_fields = ['slug']

class BlogPostSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    tags_list = serializers.ListField(
        child=serializers.CharField(),
        source='get_tags_list',
        read_only=True
    )
    
    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'content', 'excerpt', 'status',
            'category', 'category_name', 'tags', 'tags_list',
            'featured_image', 'featured_image_alt', 'meta_description',
            'reading_time', 'views', 'is_featured', 'created_at',
            'updated_at', 'published_date'
        ]
        read_only_fields = ['slug', 'views', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        """Custom create method to handle auto-publish and reading time calculation."""
        # Auto-calculate reading time if not provided
        if 'reading_time' not in validated_data:
            content = validated_data.get('content', '')
            word_count = len(content.split())
            validated_data['reading_time'] = max(1, word_count // 200)  # 200 words per minute
        
        # Auto-set status to published if not specified
        if 'status' not in validated_data:
            validated_data['status'] = 'published'
            
        return super().create(validated_data)

class BlogPostCreateSerializer(serializers.ModelSerializer):
    """Simplified serializer for automated content creation"""
    category_slug = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = BlogPost
        fields = [
            'title', 'content', 'excerpt', 'category_slug', 'tags',
            'featured_image', 'featured_image_alt', 'meta_description',
            'reading_time', 'is_featured'
        ]
    
    def create(self, validated_data):
        # Handle category by slug
        category_slug = validated_data.pop('category_slug', None)
        if category_slug:
            try:
                category = BlogCategory.objects.get(slug=category_slug)
                validated_data['category'] = category
            except BlogCategory.DoesNotExist:
                # Create category if it doesn't exist
                category = BlogCategory.objects.create(
                    name=category_slug.replace('-', ' ').title(),
                    slug=category_slug
                )
                validated_data['category'] = category
        
        # Auto-calculate reading time if not provided
        if 'reading_time' not in validated_data:
            content = validated_data.get('content', '')
            word_count = len(content.split())
            validated_data['reading_time'] = max(1, word_count // 200)
        
        # Auto-set status to published
        validated_data['status'] = 'published'
        
        return super().create(validated_data)

class NewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newsletter
        fields = ['id', 'email', 'subscribed_at', 'is_active']
        read_only_fields = ['subscribed_at']

class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['id', 'name', 'email', 'subject', 'message', 'created_at', 'is_read']
        read_only_fields = ['created_at'] 