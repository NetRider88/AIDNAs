from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import BlogPost, BlogCategory, Newsletter, ContactMessage
from .serializers import (
    BlogPostSerializer, BlogPostCreateSerializer, BlogCategorySerializer,
    NewsletterSerializer, ContactMessageSerializer
)

class BlogPostViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing blog posts.
    Supports CRUD operations for automated content creation.
    """
    queryset = BlogPost.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return BlogPostCreateSerializer
        return BlogPostSerializer
    
    def get_queryset(self):
        queryset = BlogPost.objects.all()
        
        # Filter by status
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
            
        # Filter by category
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category__slug=category)
            
        # Filter by featured
        featured = self.request.query_params.get('featured', None)
        if featured is not None:
            queryset = queryset.filter(is_featured=featured.lower() == 'true')
            
        return queryset.order_by('-created_at')
    
    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        """Publish a blog post"""
        post = self.get_object()
        post.status = 'published'
        post.published_date = timezone.now()
        post.save()
        return Response({'status': 'published'})
    
    @action(detail=True, methods=['post'])
    def unpublish(self, request, pk=None):
        """Unpublish a blog post"""
        post = self.get_object()
        post.status = 'draft'
        post.save()
        return Response({'status': 'unpublished'})
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured blog posts"""
        featured_posts = self.queryset.filter(is_featured=True, status='published')
        serializer = self.get_serializer(featured_posts, many=True)
        return Response(serializer.data)

class BlogCategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing blog categories.
    """
    queryset = BlogCategory.objects.all()
    serializer_class = BlogCategorySerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'slug'

class NewsletterViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing newsletter subscriptions.
    """
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = Newsletter.objects.all()
        
        # Filter by active status
        active = self.request.query_params.get('active', None)
        if active is not None:
            queryset = queryset.filter(is_active=active.lower() == 'true')
            
        return queryset.order_by('-subscribed_at')

class ContactMessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing contact messages.
    """
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = ContactMessage.objects.all()
        
        # Filter by read status
        read = self.request.query_params.get('read', None)
        if read is not None:
            queryset = queryset.filter(is_read=read.lower() == 'true')
            
        return queryset.order_by('-created_at')
    
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Mark a contact message as read"""
        message = self.get_object()
        message.is_read = True
        message.save()
        return Response({'status': 'marked as read'})

# Simplified API views for automation tools like n8n
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_blog_post(request):
    """
    Simplified endpoint for creating blog posts from automation tools.
    
    Expected JSON payload:
    {
        "title": "Your Blog Post Title",
        "content": "Full content of the blog post...",
        "excerpt": "Brief excerpt or summary",
        "category_slug": "ai-automation", // optional
        "tags": "AI, automation, technology", // optional
        "meta_description": "SEO description", // optional
        "is_featured": false // optional
    }
    """
    serializer = BlogPostCreateSerializer(data=request.data)
    if serializer.is_valid():
        blog_post = serializer.save()
        response_serializer = BlogPostSerializer(blog_post)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_blog_stats(request):
    """
    Get blog statistics for dashboard/monitoring.
    """
    stats = {
        'total_posts': BlogPost.objects.count(),
        'published_posts': BlogPost.objects.filter(status='published').count(),
        'draft_posts': BlogPost.objects.filter(status='draft').count(),
        'featured_posts': BlogPost.objects.filter(is_featured=True).count(),
        'total_views': sum(BlogPost.objects.values_list('views', flat=True)),
        'categories_count': BlogCategory.objects.count(),
        'newsletter_subscribers': Newsletter.objects.filter(is_active=True).count(),
        'unread_messages': ContactMessage.objects.filter(is_read=False).count(),
    }
    return Response(stats)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def bulk_create_posts(request):
    """
    Create multiple blog posts at once.
    
    Expected JSON payload:
    {
        "posts": [
            {
                "title": "Post 1",
                "content": "Content 1...",
                ...
            },
            {
                "title": "Post 2", 
                "content": "Content 2...",
                ...
            }
        ]
    }
    """
    posts_data = request.data.get('posts', [])
    created_posts = []
    errors = []
    
    for i, post_data in enumerate(posts_data):
        serializer = BlogPostCreateSerializer(data=post_data)
        if serializer.is_valid():
            blog_post = serializer.save()
            created_posts.append(BlogPostSerializer(blog_post).data)
        else:
            errors.append({'index': i, 'errors': serializer.errors})
    
    response_data = {
        'created_count': len(created_posts),
        'error_count': len(errors),
        'created_posts': created_posts,
        'errors': errors
    }
    
    return Response(response_data, status=status.HTTP_207_MULTI_STATUS)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])  # Allow public access
def api_health(request):
    """
    Public health check endpoint for monitoring.
    """
    return Response({
        'status': 'healthy',
        'timestamp': timezone.now(),
        'version': '1.0'
    }) 