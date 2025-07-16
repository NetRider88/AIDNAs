from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import BlogPost, BlogCategory

# Create your views here.

def blog_list(request):
    """
    Main blog page with search and filtering
    """
    # Get search query
    search_query = request.GET.get('search', '')
    
    # Base queryset - only published posts
    posts = BlogPost.objects.filter(status='published')
    
    # Apply search filter
    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(excerpt__icontains=search_query) |
            Q(tags__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(posts, 6)  # 6 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get featured posts for sidebar
    featured_posts = BlogPost.objects.filter(
        status='published', 
        is_featured=True
    )[:3]
    
    # Get all categories
    categories = BlogCategory.objects.all()
    
    # Get popular tags (simplified - just get all unique tags)
    all_posts = BlogPost.objects.filter(status='published').exclude(tags='')
    all_tags = []
    for post in all_posts:
        all_tags.extend(post.get_tags_list())
    popular_tags = list(set(all_tags))[:10]  # Top 10 unique tags
    
    context = {
        'page_obj': page_obj,
        'featured_posts': featured_posts,
        'categories': categories,
        'popular_tags': popular_tags,
        'search_query': search_query,
    }
    return render(request, 'blog/blog_list.html', context)

def blog_detail(request, slug):
    """
    Individual blog post detail page
    """
    post = get_object_or_404(BlogPost, slug=slug, status='published')
    
    # Increment view count
    post.views += 1
    post.save(update_fields=['views'])
    
    # Get related posts (same category)
    related_posts = BlogPost.objects.filter(
        status='published',
        category=post.category
    ).exclude(id=post.id)[:3]
    
    # Get previous and next posts
    previous_post = BlogPost.objects.filter(
        status='published',
        published_date__lt=post.published_date
    ).first()
    
    next_post = BlogPost.objects.filter(
        status='published',
        published_date__gt=post.published_date
    ).last()
    
    context = {
        'post': post,
        'related_posts': related_posts,
        'previous_post': previous_post,
        'next_post': next_post,
    }
    return render(request, 'blog/blog_detail.html', context)

def blog_by_category(request, category_slug):
    """
    Blog posts filtered by category
    """
    category = get_object_or_404(BlogCategory, slug=category_slug)
    posts = BlogPost.objects.filter(status='published', category=category)
    
    # Pagination
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'page_obj': page_obj,
    }
    return render(request, 'blog/blog_by_category.html', context)

def blog_by_tag(request, tag):
    """
    Blog posts filtered by tag
    """
    posts = BlogPost.objects.filter(
        status='published', 
        tags__icontains=tag
    )
    
    # Pagination
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'tag': tag,
        'page_obj': page_obj,
    }
    return render(request, 'blog/blog_by_tag.html', context)
