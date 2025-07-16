from django.db import models

# Create your models here.

class Profile(models.Model):
    """
    Main profile information that appears across the site
    """
    name = models.CharField(max_length=100, default="AI DNAs / John")
    title = models.CharField(max_length=200, default="AI Developer & Automation Specialist")
    tagline = models.CharField(max_length=300, default="Automating the Future: One Bot at a Time")
    bio = models.TextField(help_text="Brief intro about yourself")
    detailed_bio = models.TextField(help_text="Detailed bio for About page")
    
    # Contact Information
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    
    # Files
    cv_file = models.FileField(upload_to='documents/', blank=True, help_text="Downloadable CV")
    profile_image = models.ImageField(upload_to='profile/', blank=True)
    
    # SEO
    meta_description = models.CharField(max_length=160, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profile"
    
    def __str__(self):
        return self.name

class Achievement(models.Model):
    """
    Key achievements for the recruiter page
    """
    title = models.CharField(max_length=200)
    description = models.TextField()
    metric = models.CharField(max_length=100, blank=True, help_text="e.g., '94% email reach'")
    company = models.CharField(max_length=100, blank=True)
    date = models.DateField()
    order = models.PositiveIntegerField(default=0, help_text="Display order")
    
    class Meta:
        ordering = ['order', '-date']
    
    def __str__(self):
        return self.title

class Skill(models.Model):
    """
    Technical skills and tools
    """
    SKILL_CATEGORIES = [
        ('programming', 'Programming Languages'),
        ('frameworks', 'Frameworks & Libraries'),
        ('tools', 'Tools & Platforms'),
        ('databases', 'Databases'),
        ('ai_ml', 'AI/ML Technologies'),
    ]
    
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=SKILL_CATEGORIES)
    proficiency = models.PositiveIntegerField(default=5, help_text="1-10 scale")
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['category', 'order', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"

class Testimonial(models.Model):
    """
    Client/colleague testimonials
    """
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=200)
    company = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to='testimonials/', blank=True)
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'name']
    
    def __str__(self):
        return f"{self.name} - {self.company}"
