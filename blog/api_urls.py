from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

# Create a router and register our viewsets
router = DefaultRouter()
router.register(r'posts', api_views.BlogPostViewSet, basename='blogpost')
router.register(r'categories', api_views.BlogCategoryViewSet, basename='blogcategory')
router.register(r'newsletter', api_views.NewsletterViewSet, basename='newsletter')
router.register(r'messages', api_views.ContactMessageViewSet, basename='contactmessage')

# Define URL patterns
urlpatterns = [
    # Router URLs (includes all CRUD operations)
    path('', include(router.urls)),
    
    # Custom simplified endpoints for automation
    path('create-post/', api_views.create_blog_post, name='create-blog-post'),
    path('bulk-create/', api_views.bulk_create_posts, name='bulk-create-posts'),
    path('stats/', api_views.get_blog_stats, name='blog-stats'),
    path('health/', api_views.api_health, name='api-health'),
] 