from django.contrib import admin
from .models import ProjectCategory, Technology, Project, ProjectImage, ProjectUpdate

@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'order']
    list_editable = ['order']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'icon']
    search_fields = ['name']

class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1
    fields = ['image', 'caption', 'order']

class ProjectUpdateInline(admin.TabularInline):
    model = ProjectUpdate
    extra = 0
    fields = ['title', 'content', 'image', 'created_at']
    readonly_fields = ['created_at']

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'start_date', 'launch_date', 'is_featured', 'order']
    list_editable = ['status', 'is_featured', 'order']
    list_filter = ['status', 'categories', 'technologies', 'is_featured']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ['categories', 'technologies']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'tagline', 'short_description', 'description')
        }),
        ('Status & Categorization', {
            'fields': ('status', 'categories', 'technologies')
        }),
        ('Dates', {
            'fields': ('start_date', 'launch_date', 'expected_launch')
        }),
        ('Links', {
            'fields': ('live_url', 'github_url', 'demo_url')
        }),
        ('Media', {
            'fields': ('featured_image', 'logo')
        }),
        ('Impact & Metrics', {
            'fields': ('key_metrics', 'user_impact')
        }),
        ('Display Options', {
            'fields': ('is_featured', 'order')
        }),
        ('SEO', {
            'fields': ('meta_description',),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [ProjectImageInline, ProjectUpdateInline]

@admin.register(ProjectUpdate)
class ProjectUpdateAdmin(admin.ModelAdmin):
    list_display = ['project', 'title', 'created_at']
    list_filter = ['project', 'created_at']
    search_fields = ['title', 'content']
