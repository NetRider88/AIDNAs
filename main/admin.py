from django.contrib import admin
from .models import Profile, Achievement, Skill, Testimonial

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'email', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'title', 'tagline', 'bio', 'detailed_bio')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'linkedin_url', 'github_url')
        }),
        ('Files & Media', {
            'fields': ('profile_image', 'cv_file')
        }),
        ('SEO', {
            'fields': ('meta_description',),
            'classes': ('collapse',)
        }),
    )

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'metric', 'date', 'order']
    list_editable = ['order']
    list_filter = ['company', 'date']
    ordering = ['order', '-date']

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'proficiency', 'order']
    list_editable = ['proficiency', 'order']
    list_filter = ['category']
    ordering = ['category', 'order']

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'position', 'is_featured', 'order']
    list_editable = ['is_featured', 'order']
    list_filter = ['is_featured', 'company']
    ordering = ['order']
