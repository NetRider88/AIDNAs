from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Project, ProjectCategory, Technology

# Create your views here.

def project_list(request):
    """
    Main projects page with filtering by status and category
    """
    # Filter parameters
    status_filter = request.GET.get('status', '')
    category_filter = request.GET.get('category', '')
    tech_filter = request.GET.get('tech', '')
    
    # Base queryset
    projects = Project.objects.all()
    
    # Apply filters
    if status_filter:
        projects = projects.filter(status=status_filter)
    
    if category_filter:
        projects = projects.filter(categories__slug=category_filter)
    
    if tech_filter:
        projects = projects.filter(technologies__name__icontains=tech_filter)
    
    # Organize by status
    live_projects = projects.filter(status='live')
    in_progress_projects = projects.filter(status='in_progress')
    planned_projects = projects.filter(status='planned')
    
    # Get all categories and technologies for filtering
    categories = ProjectCategory.objects.all()
    technologies = Technology.objects.all()
    
    # Status choices for filter
    status_choices = Project.STATUS_CHOICES
    
    context = {
        'live_projects': live_projects,
        'in_progress_projects': in_progress_projects,
        'planned_projects': planned_projects,
        'categories': categories,
        'technologies': technologies,
        'status_choices': status_choices,
        'current_filters': {
            'status': status_filter,
            'category': category_filter,
            'tech': tech_filter,
        }
    }
    return render(request, 'projects/project_list.html', context)

def project_detail(request, slug):
    """
    Individual project detail page
    """
    project = get_object_or_404(Project, slug=slug)
    
    # Get related projects (same categories)
    related_projects = Project.objects.filter(
        categories__in=project.categories.all()
    ).exclude(id=project.id).distinct()[:3]
    
    context = {
        'project': project,
        'related_projects': related_projects,
    }
    return render(request, 'projects/project_detail.html', context)

def projects_by_category(request, category_slug):
    """
    Projects filtered by specific category
    """
    category = get_object_or_404(ProjectCategory, slug=category_slug)
    projects = Project.objects.filter(categories=category)
    
    # Organize by status
    live_projects = projects.filter(status='live')
    in_progress_projects = projects.filter(status='in_progress')
    planned_projects = projects.filter(status='planned')
    
    context = {
        'category': category,
        'live_projects': live_projects,
        'in_progress_projects': in_progress_projects,
        'planned_projects': planned_projects,
    }
    return render(request, 'projects/projects_by_category.html', context)
