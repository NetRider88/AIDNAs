from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

class BlogCategory(models.Model):
    """
    Blog post categories (Product Updates, How-Tos, AI Insights, Behind the Scenes)
    """
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default="#8B5CF6", help_text="Hex color code")
    icon = models.CharField(max_length=50, blank=True, help_text="Font Awesome icon class")
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = "Blog Categories"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class BlogPost(models.Model):
    """
    Blog posts for sharing product updates, AI thoughts, tutorials, etc.
    """
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    excerpt = models.CharField(max_length=500, help_text="Brief summary for previews")
    content = models.TextField(help_text="Main blog content (Markdown supported)")
    
    # Categorization
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.CharField(max_length=500, blank=True, help_text="Comma-separated tags")
    
    # Media
    featured_image = models.ImageField(upload_to='blog/featured/', blank=True)
    featured_image_alt = models.CharField(max_length=200, blank=True, help_text="Alt text for accessibility")
    
    # Publishing
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    published_date = models.DateTimeField(blank=True, null=True)
    
    # SEO
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)
    
    # Engagement
    views = models.PositiveIntegerField(default=0)
    reading_time = models.PositiveIntegerField(default=5, help_text="Estimated reading time in minutes")
    
    # Display options
    is_featured = models.BooleanField(default=False, help_text="Feature on homepage")
    allow_comments = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-published_date', '-created_at']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return f"/blog/{self.slug}/"
    
    def get_tags_list(self):
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]

class Newsletter(models.Model):
    """
    Newsletter subscribers
    """
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    subscribed_date = models.DateTimeField(auto_now_add=True)
    
    # Preferences
    weekly_updates = models.BooleanField(default=True)
    product_updates = models.BooleanField(default=True)
    ai_insights = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-subscribed_date']
    
    def __str__(self):
        return self.email

class ContactMessage(models.Model):
    """
    Contact form submissions
    """
    MESSAGE_TYPES = [
        ('general', 'General Inquiry'),
        ('project', 'Project Collaboration'),
        ('interview', 'Interview Request'),
        ('speaking', 'Speaking Opportunity'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    company = models.CharField(max_length=100, blank=True)
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPES, default='general')
    subject = models.CharField(max_length=200)
    message = models.TextField()
    
    # Status tracking
    is_read = models.BooleanField(default=False)
    is_replied = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.subject}"
