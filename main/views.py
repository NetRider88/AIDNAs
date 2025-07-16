from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from .models import Profile, Achievement, Skill, Testimonial
from projects.models import Project
from blog.models import BlogPost, Newsletter, ContactMessage

def home(request):
    """
    Homepage with intro, featured projects, and latest blog posts
    """
    try:
        profile = Profile.objects.first()
    except Profile.DoesNotExist:
        profile = None
    
    # Featured projects
    featured_projects = Project.objects.filter(is_featured=True, status='live')[:3]
    
    # Latest blog posts
    latest_posts = BlogPost.objects.filter(status='published')[:3]
    
    # Featured testimonials
    featured_testimonials = Testimonial.objects.filter(is_featured=True)[:2]
    
    context = {
        'profile': profile,
        'featured_projects': featured_projects,
        'latest_posts': latest_posts,
        'featured_testimonials': featured_testimonials,
    }
    return render(request, 'main/home.html', context)

def about(request):
    """
    About page with detailed bio, skills, and achievements
    """
    try:
        profile = Profile.objects.first()
    except Profile.DoesNotExist:
        profile = None
    
    # Skills organized by category
    skills_by_category = {}
    for skill in Skill.objects.all():
        category = skill.get_category_display()
        if category not in skills_by_category:
            skills_by_category[category] = []
        skills_by_category[category].append(skill)
    
    # All testimonials
    testimonials = Testimonial.objects.all()
    
    context = {
        'profile': profile,
        'skills_by_category': skills_by_category,
        'testimonials': testimonials,
    }
    return render(request, 'main/about.html', context)

def recruiter(request):
    """
    Recruiter-focused page with achievements and downloadable CV
    """
    try:
        profile = Profile.objects.first()
    except Profile.DoesNotExist:
        profile = None
    
    # Key achievements
    achievements = Achievement.objects.all()
    
    # Live projects with metrics
    live_projects = Project.objects.filter(status='live').exclude(key_metrics='')
    
    # Key skills
    key_skills = Skill.objects.filter(proficiency__gte=7)
    
    context = {
        'profile': profile,
        'achievements': achievements,
        'live_projects': live_projects,
        'key_skills': key_skills,
    }
    return render(request, 'main/recruiter.html', context)

def contact(request):
    """
    Contact page with form handling
    """
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        company = request.POST.get('company', '')
        message_type = request.POST.get('message_type', 'general')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Save contact message
        contact_message = ContactMessage.objects.create(
            name=name,
            email=email,
            company=company,
            message_type=message_type,
            subject=subject,
            message=message,
        )
        
        # Send email notification to admin
        try:
            print(f"📧 Attempting to send contact email to {settings.ADMIN_EMAIL}")
            admin_subject = f"New Contact Message: {subject}"
            admin_message = f"""
New contact message received from AI DNAs website:

Name: {name}
Email: {email}
Company: {company}
Type: {contact_message.get_message_type_display()}
Subject: {subject}

Message:
{message}

---
Sent from AI DNAs Portfolio Website
            """
            
            send_mail(
                subject=admin_subject,
                message=admin_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=False,
            )
            print("✅ Contact email sent successfully!")
        except Exception as e:
            print(f"❌ Failed to send contact notification email: {e}")
            print(f"📧 Email settings: {settings.EMAIL_HOST_USER} -> {settings.ADMIN_EMAIL}")
        
        messages.success(request, 'Thank you for your message! I will get back to you soon.')
        return redirect('main:contact')
    
    try:
        profile = Profile.objects.first()
    except Profile.DoesNotExist:
        profile = None
    
    context = {
        'profile': profile,
        'message_types': ContactMessage.MESSAGE_TYPES,
    }
    return render(request, 'main/contact.html', context)

def newsletter_signup(request):
    """
    Newsletter signup endpoint (AJAX)
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name', '')
        
        if email:
            newsletter, created = Newsletter.objects.get_or_create(
                email=email,
                defaults={'name': name}
            )
            
            if created:
                # Send email notification to admin about new subscriber
                try:
                    print(f"📧 Attempting to send newsletter email to {settings.ADMIN_EMAIL}")
                    admin_subject = "New Newsletter Subscription - AI DNAs"
                    admin_message = f"""
New newsletter subscription received:

Email: {email}
Name: {name if name else 'Not provided'}
Subscribed: {newsletter.subscribed_date.strftime('%Y-%m-%d %H:%M:%S')}

Total subscribers: {Newsletter.objects.filter(is_active=True).count()}

---
Sent from AI DNAs Portfolio Website
                    """
                    
                    send_mail(
                        subject=admin_subject,
                        message=admin_message,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[settings.ADMIN_EMAIL],
                        fail_silently=False,
                    )
                    print("✅ Newsletter email sent successfully!")
                except Exception as e:
                    print(f"❌ Failed to send newsletter notification email: {e}")
                    print(f"📧 Email settings: {settings.EMAIL_HOST_USER} -> {settings.ADMIN_EMAIL}")
                
                return JsonResponse({'success': True, 'message': 'Successfully subscribed!'})
            else:
                return JsonResponse({'success': False, 'message': 'Email already subscribed.'})
        
        return JsonResponse({'success': False, 'message': 'Please provide a valid email.'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})
