from django.contrib import admin
from .models import BlogCategory, BlogPost, Newsletter, ContactMessage

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'order']
    list_editable = ['order']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status', 'published_date', 'is_featured', 'views']
    list_editable = ['status', 'is_featured']
    list_filter = ['status', 'category', 'is_featured', 'published_date']
    search_fields = ['title', 'content', 'excerpt']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_date'
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'excerpt', 'content')
        }),
        ('Categorization', {
            'fields': ('category', 'tags')
        }),
        ('Media', {
            'fields': ('featured_image', 'featured_image_alt')
        }),
        ('Publishing', {
            'fields': ('status', 'author', 'published_date')
        }),
        ('Settings', {
            'fields': ('is_featured', 'allow_comments', 'reading_time')
        }),
        ('SEO', {
            'fields': ('meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('Stats', {
            'fields': ('views',),
            'classes': ('collapse',)
        }),
    )

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'is_active', 'subscribed_date']
    list_editable = ['is_active']
    list_filter = ['is_active', 'weekly_updates', 'product_updates', 'ai_insights']
    search_fields = ['email', 'name']
    date_hierarchy = 'subscribed_date'

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'message_type', 'subject', 'is_read', 'is_replied', 'created_at']
    list_editable = ['is_read', 'is_replied']
    list_filter = ['message_type', 'is_read', 'is_replied', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at']
