from django.db import models
from django.utils.text import slugify

class ProjectCategory(models.Model):
    """
    Categories for organizing projects (CRM, Education, Finance, Marketing, etc.)
    """
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Font Awesome icon class")
    color = models.CharField(max_length=7, default="#3B82F6", help_text="Hex color code")
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = "Project Categories"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class Technology(models.Model):
    """
    Technologies used in projects
    """
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, blank=True, help_text="Font Awesome or tech icon class")
    color = models.CharField(max_length=7, default="#10B981", help_text="Hex color code")
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = "Technologies"
    
    def __str__(self):
        return self.name

class Project(models.Model):
    """
    AI-Dnas projects with live, in-progress, and planned statuses
    """
    STATUS_CHOICES = [
        ('live', 'Live'),
        ('in_progress', 'In Progress'),
        ('planned', 'Planned'),
        ('paused', 'Paused'),
    ]
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    tagline = models.CharField(max_length=300, blank=True, help_text="Brief one-liner")
    description = models.TextField(help_text="Detailed project description")
    short_description = models.CharField(max_length=500, help_text="For project cards")
    
    # Status and categorization
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')
    categories = models.ManyToManyField(ProjectCategory, blank=True)
    technologies = models.ManyToManyField(Technology, blank=True)
    
    # Project details
    start_date = models.DateField()
    launch_date = models.DateField(blank=True, null=True)
    expected_launch = models.DateField(blank=True, null=True, help_text="For in-progress projects")
    
    # Links and media
    live_url = models.URLField(blank=True, help_text="Live project URL")
    github_url = models.URLField(blank=True)
    demo_url = models.URLField(blank=True)
    
    # Images
    featured_image = models.ImageField(upload_to='projects/featured/', blank=True)
    logo = models.ImageField(upload_to='projects/logos/', blank=True)
    
    # Metrics and achievements
    key_metrics = models.TextField(blank=True, help_text="Key achievements or metrics")
    user_impact = models.CharField(max_length=500, blank=True, help_text="How it helps users")
    
    # Display options
    is_featured = models.BooleanField(default=False, help_text="Show on homepage")
    order = models.PositiveIntegerField(default=0, help_text="Display order")
    
    # SEO
    meta_description = models.CharField(max_length=160, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', '-created_at']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name} ({self.get_status_display()})"
    
    def get_absolute_url(self):
        return f"/projects/{self.slug}/"

class ProjectImage(models.Model):
    """
    Additional images/screenshots for projects
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='projects/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.project.name} - Image {self.order}"

class ProjectUpdate(models.Model):
    """
    Progress updates for in-progress projects
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='updates')
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='projects/updates/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.project.name} - {self.title}"
