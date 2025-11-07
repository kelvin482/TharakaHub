from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from datetime import datetime
from decimal import Decimal, InvalidOperation
from django.utils import timezone
from jobs.models import Job
from .models import Profile, UserProject

#application part
from django.db import models
from jobs.models import Application  # ensure import path is correct


def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if username and password:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, "Registration successful! Please login.")
            return redirect('users:login')
        else:
            messages.error(request, "Please provide username and password.")
    return render(request, 'users/register.html')


def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('users:home')
        else:
            messages.error(request, "Invalid credentials")
    return render(request, 'users/login.html')


@login_required
def home(request):
    # Get recent assignments
    recent_assignments = [
        {
            'title': 'Data Structures Assignment',
            'price': '2,500',
            'deadline': '3 days',
            'department': 'Computer Science'
        },
        {
            'title': 'Marketing Strategy Analysis',
            'price': '3,000',
            'deadline': '5 days',
            'department': 'Business'
        }
    ]
    
    # Get recent blog posts
    recent_posts = [
        {
            'title': 'Study Tips for Finals',
            'excerpt': 'Proven techniques to improve retention and exam performance.',
            'category': 'Study Guides',
        },
        {
            'title': 'How to Price Your Assignment',
            'excerpt': 'A quick guide to setting a fair price for posted assignments.',
            'category': 'Business',
        }
    ]
    
    context = {
        'recent_assignments': recent_assignments,
        'recent_posts': recent_posts,
        'total_assignments': 150,  # Example statistics
        'active_users': 1200,
        'success_rate': 98
    }
    return render(request, 'users/home.html', context)


def logout_user(request):
    logout(request)
    return redirect('users:login')


@login_required
def dashboard(request):
    # Get or create user profile
    user_profile, created = Profile.objects.get_or_create(user=request.user)
    
    # Sample data for the freelancer dashboard
    notifications = [
        {'text': 'New message from client Alice', 'time': '2h'},
        {'text': 'Payment received for Project X', 'time': '1d'},
    ]

    context = {
        'user_profile': user_profile,  # Pass the profile to template
        'notifications': notifications,
        'notif_count': len(notifications),
        'progress_percent': 72,
        'new_opportunities': [
            {'title': 'UI Design for Mobile App', 'price': '5,000'},
            {'title': 'Research Article Editing', 'price': '3,000'},
        ],
        'earnings': {
            'balance': '12,450',
            'monthly': '3,200',
        },
        'tasks': [
            {'title': 'Submit draft for Project X', 'due': 'Today'},
            {'title': 'Review client feedback', 'due': 'Tomorrow'},
        ],
        # Overview metrics and sample projects
        'total_projects': 24,
        'total_earnings': '40450',
        'ongoing_projects': 6,
        'avg_rating': 4.7,
        'projects': [
            {'name': 'Project X', 'client': 'Alice', 'status': 'In Progress', 'deadline': '2025-11-10', 'payment_status': 'Partial', 'progress': 60},
            {'name': 'Brand Refresh', 'client': 'Beta Co', 'status': 'Pending', 'deadline': '2025-12-01', 'payment_status': 'Unpaid', 'progress': 10},
            {'name': 'Mobile App UI', 'client': 'Gamma Ltd', 'status': 'Completed', 'deadline': '2025-09-21', 'payment_status': 'Paid', 'progress': 100},
        ]
    }

    return render(request, 'users/dashboard.html', context)


def jobs(request):
    # Fetch all active posted jobs
    jobs_qs = Job.objects.filter(status=Job.Status.POSTED, is_active=True).order_by('-created_at')
    
    # Group jobs by department
    departments_data = {}
    department_names = {
        'computer-science': 'Computer Science',
        'business': 'Business',
        'education': 'Education',
        'nursing': 'Nursing',
        'engineering': 'Engineering'
    }
    
    # Initialize all departments
    for dept_key, dept_name in department_names.items():
        departments_data[dept_key] = {
            'name': dept_name,
            'jobs': []
        }
    
    # Group jobs by department
    for job in jobs_qs:
        # Normalize department key: handle both "computer-science" and "Computer Science" formats
        dept_key = job.department.lower().strip().replace(' ', '-')
        if dept_key in departments_data:
            departments_data[dept_key]['jobs'].append(job)
        else:
            # Fallback: try to match by department name
            for key, dept_info in departments_data.items():
                if dept_info['name'].lower() == job.department.lower().strip():
                    departments_data[key]['jobs'].append(job)
                    break
    
    # Calculate days until deadline for each job
    for dept_data in departments_data.values():
        for job in dept_data['jobs']:
            days_left = (job.deadline - timezone.now().date()).days
            job.days_left = days_left if days_left >= 0 else 0
    
    context = {
        'departments': departments_data,
        'total_jobs': jobs_qs.count()
    }
    
    return render(request, 'jobs/jobs.html', context)


@login_required
def create_assignment(request):
    return redirect('jobs:create')


def blog_list(request):
    # Temporary sample posts so the template can render without DB data
    sample_posts = [
        {
            'title': 'Welcome to Student Helper',
            'slug': 'welcome-to-student-helper',
            'excerpt': 'An introduction to the platform and how to get started.',
            'author': 'Admin',
            'created_at': datetime.now(),
            'category': 'Announcements',
            'image': None,
        },
        {
            'title': 'Study Tips for Finals',
            'slug': 'study-tips-for-finals',
            'excerpt': 'Proven techniques to improve retention and exam performance.',
            'author': 'Kelvin',
            'created_at': datetime.now(),
            'category': 'Study Guides',
            'image': None,
        },
        {
            'title': 'How to Price Your Assignment',
            'slug': 'how-to-price-your-assignment',
            'excerpt': 'A quick guide to setting a fair price for posted assignments.',
            'author': 'Kelvin',
            'created_at': datetime.now(),
            'category': 'Business',
            'image': None,
        }
    ]
    return render(request, 'users/blog_list.html', {'posts': sample_posts})


def blog_detail(request, slug):
    # Use the same sample posts used by blog_list for local dev
    sample_posts = [
        {
            'title': 'Welcome to Student Helper',
            'slug': 'welcome-to-student-helper',
            'excerpt': 'An introduction to the platform and how to get started.',
            'author': 'Admin',
            'created_at': datetime.now(),
            'category': 'Announcements',
            'image': None,
            'content': '<p>This is a sample blog post content. Replace with DB content.</p>'
        },
        {
            'title': 'Study Tips for Finals',
            'slug': 'study-tips-for-finals',
            'excerpt': 'Proven techniques to improve retention and exam performance.',
            'author': 'Kelvin',
            'created_at': datetime.now(),
            'category': 'Study Guides',
            'image': None,
            'content': '<p>Study smart: break sessions into focused intervals and practice active recall.</p>'
        },
        {
            'title': 'How to Price Your Assignment',
            'slug': 'how-to-price-your-assignment',
            'excerpt': 'A quick guide to setting a fair price for posted assignments.',
            'author': 'Kelvin',
            'created_at': datetime.now(),
            'category': 'Business',
            'image': None,
            'content': '''
                <p>Setting the right price for your assignment is crucial for attracting the right talent while ensuring fair compensation. Here are some key factors to consider:</p>
                <h2>Factors to Consider</h2>
                <ul>
                    <li><strong>Complexity:</strong> More complex assignments require higher prices</li>
                    <li><strong>Deadline:</strong> Urgent deadlines often command premium rates</li>
                    <li><strong>Subject Matter:</strong> Specialized fields may have higher market rates</li>
                    <li><strong>Word Count/Pages:</strong> Longer assignments typically cost more</li>
                </ul>
                <h2>Pricing Guidelines</h2>
                <p>Start by researching similar assignments in your field. Consider the time investment required and the expertise level needed. A good rule of thumb is to base your price on:</p>
                <ol>
                    <li>Estimated hours of work required</li>
                    <li>Standard hourly rates for your academic level</li>
                    <li>Complexity and urgency factors</li>
                </ol>
                <p>Remember, fair pricing attracts quality work and helps build trust with freelancers.</p>
            '''
        }
    ]

    post = next((p for p in sample_posts if p['slug'] == slug), None)
    if not post:
        raise Http404('Post not found')
    return render(request, 'users/blog_detail.html', {'post': post, 'related_posts': sample_posts[:3]})

  # dashboard navpages
  
@login_required
def projects(request):
    user = request.user
    # Handle new project creation (POST to same endpoint)
    if request.method == 'POST':
        title = (request.POST.get('title') or '').strip()
        description = (request.POST.get('description') or '').strip()
        try:
            progress = int(request.POST.get('progress', '0'))
        except Exception:
            progress = 0
        progress = max(0, min(100, progress))
        # Derive status for convenience; user-supplied status is optional
        if progress >= 100:
            status = 'Completed'
        elif progress <= 0:
            status = 'Pending'
        else:
            status = 'In Progress'
        if title:
            UserProject.objects.create(
                owner=user,
                title=title,
                description=description,
                progress=progress,
                status=status,
            )
    jobs_qs = (
        Job.objects
        .filter(models.Q(assignee=user) | models.Q(poster=user))
        .order_by('-updated_at')
    )

    def status_to_progress(status):
        if status == Job.Status.COMPLETED:
            return 100
        if status == Job.Status.IN_PROGRESS:
            return 60
        if status == Job.Status.POSTED:
            return 10
        return 0

    # Personal dashboard projects (user created)
    user_projects = [
        {
            'title': p.title,
            'description': p.description,
            'progress': p.progress,
            'status': p.status,
        }
        for p in UserProject.objects.filter(owner=user)
    ]

    projects = [
        {
            'title': job.title,
            'description': job.description[:160] + ('…' if len(job.description) > 160 else ''),
            'progress': status_to_progress(job.status),
            'status': job.get_status_display(),
        }
        for job in jobs_qs
    ]

    # Merge user-created projects first, then job-derived
    all_projects = user_projects + projects

    return render(request, 'users/dashboardfiles/projects.html', {'projects': all_projects})

@login_required
def clients(request):
    """Display clients from jobs the user has applied for"""
    # Get all jobs where the current user is the assignee (applied jobs)
    applied_jobs = Job.objects.filter(assignee=request.user).select_related('poster').order_by('-created_at')
    
    # Group jobs by client (poster) to get unique clients
    clients_data = {}
    for job in applied_jobs:
        client_id = job.poster.id
        if client_id not in clients_data:
            # Get client profile if available
            client_profile = None
            try:
                client_profile = job.poster.profile
            except:
                pass
            
            clients_data[client_id] = {
                'id': client_id,
                'name': job.poster.get_full_name() or job.poster.username,
                'username': job.poster.username,
                'email': job.poster.email or 'No email',
                'phone': getattr(client_profile, 'phone_number', 'Not provided') if client_profile else 'Not provided',
                'company': getattr(client_profile, 'location', 'Not specified') if client_profile else 'Not specified',
                'photo_url': client_profile.profile_picture.url if client_profile and client_profile.profile_picture else None,
                'jobs': [],
                'projects_count': 0,
            }
        
        # Add job to client's jobs list
        clients_data[client_id]['jobs'].append({
            'id': job.id,
            'title': job.title,
            'status': job.status,
            'status_display': job.get_status_display(),
            'deadline': job.deadline,
            'price': job.price,
            'department': job.department,
        })
        clients_data[client_id]['projects_count'] = len(clients_data[client_id]['jobs'])
    
    # Convert to list for template
    clients_list = list(clients_data.values())
    
    # Calculate statistics
    total_clients = len(clients_list)
    active_clients = len([c for c in clients_list if any(j['status'] in ['IN_PROGRESS', 'POSTED'] for j in c['jobs'])])
    projects_in_progress = len([j for client in clients_list for j in client['jobs'] if j['status'] == 'IN_PROGRESS'])
    
    context = {
        'clients': clients_list,
        'total_clients': total_clients,
        'active_clients': active_clients,
        'projects_in_progress': projects_in_progress,
    }
    
    return render(request, 'users/dashboardfiles/clients.html', context)

@login_required
def messages_view(request):
    user = request.user
    apps = (
        Application.objects
        .filter(models.Q(applicant=user) | models.Q(job__poster=user))
        .select_related('job', 'applicant', 'job__poster')
        .order_by('-submitted_at')[:20]
    )

    inbox_messages = []
    for app in apps:
        counterpart = app.job.poster if app.applicant == user else app.applicant
        inbox_messages.append({
            'sender': counterpart.get_full_name() or counterpart.username,
            'preview': (app.cover_letter or f"Application for {app.job.title}")[:60],
            'timestamp': app.submitted_at.strftime('%Y-%m-%d %H:%M'),
        })

    return render(request, 'users/dashboardfiles/messages.html', {'inbox_messages': inbox_messages})

@login_required
def earnings(request):
    user = request.user
    tz_now = timezone.now()
    month_start = tz_now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    assigned_jobs = Job.objects.filter(assignee=user)

    total_this_month = (
        assigned_jobs
        .filter(status=Job.Status.COMPLETED, updated_at__gte=month_start)
        .aggregate(s=models.Sum('price'))['s'] or 0
    )
    pending_total = (
        assigned_jobs
        .filter(status__in=[Job.Status.POSTED, Job.Status.IN_PROGRESS])
        .aggregate(s=models.Sum('price'))['s'] or 0
    )

    withdrawn = 0
    available_balance = max((assigned_jobs.filter(status=Job.Status.COMPLETED)
                              .aggregate(s=models.Sum('price'))['s'] or 0) - withdrawn, 0)

    transactions = [
        {
            'date': j.updated_at.date(),
            'client': j.poster.get_full_name() or j.poster.username,
            'project': j.title,
            'amount': j.price,
            'status': 'Paid' if j.status == Job.Status.COMPLETED else 'Pending',
            'method': 'Bank',
        }
        for j in assigned_jobs.order_by('-updated_at')[:20]
    ]

    context = {
        'total_earnings_month': total_this_month,
        'pending_payments': pending_total,
        'withdrawn_total': withdrawn,
        'available_balance': available_balance,
        'transactions': transactions,
    }

    return render(request, 'users/dashboardfiles/earnings.html', context)

@login_required
def portfolio(request):
    user = request.user
    completed = Job.objects.filter(assignee=user, status=Job.Status.COMPLETED).order_by('-updated_at')
    portfolio_items = [
        {
            'title': j.title,
            'tags': [j.department, j.unit] if j.unit else [j.department],
            'completed_at': j.updated_at.date(),
            'image_url': None,
        }
        for j in completed[:12]
    ]
    return render(request, 'users/dashboardfiles/portfolio.html', {'portfolio': portfolio_items})

@login_required
def settings(request):
    """User settings page - handle profile updates"""
    # Get or create user profile
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        try:
            # Update profile fields
            profile.first_name = request.POST.get('first_name', '').strip()
            profile.last_name = request.POST.get('last_name', '').strip()
            profile.bio = request.POST.get('bio', '').strip()
            profile.phone_number = request.POST.get('phone_number', '').strip()
            profile.location = request.POST.get('location', '').strip()
            profile.address = request.POST.get('address', '').strip()
            profile.website = request.POST.get('website', '').strip()
            profile.github = request.POST.get('github', '').strip()
            profile.linkedin = request.POST.get('linkedin', '').strip()
            profile.twitter = request.POST.get('twitter', '').strip()
            
            # Handle notification preferences
            profile.notification_email = 'notification_email' in request.POST
            profile.notification_push = 'notification_push' in request.POST
            
            # Handle profile picture upload
            if 'profile_picture' in request.FILES:
                profile.profile_picture = request.FILES['profile_picture']
            
            # Update user email if provided
            user_email = request.POST.get('email', '').strip()
            if user_email:
                if user_email != request.user.email:
                    request.user.email = user_email
                    request.user.save()
            
            # Save the profile
            profile.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('users:settings')
        except Exception as e:
            messages.error(request, f'Error updating profile: {str(e)}')
    
    # Get user's profile data
    context = {
        'profile': profile,
        'user': request.user,
    }
    
    return render(request, 'users/dashboardfiles/settings.html', context)

#dashboard project
def projects_view(request):
    projects = [
        {'title': 'AI Chatbot', 'description': 'A chatbot that answers FAQs.', 'progress': 75, 'status': 'In Progress'},
        {'title': 'University Portal', 'description': 'Frontend for the university system.', 'progress': 40, 'status': 'Ongoing'},
        {'title': 'Portfolio Website', 'description': 'Personal portfolio with blog integration.', 'progress': 100, 'status': 'Completed'},
    ]
    return render(request, 'users/dashboardfiles/projects.html', {'projects': projects})


@login_required
def clients_view(request):
    """Display clients from jobs the user has applied for"""
    # Get all jobs where the current user is the assignee (applied jobs)
    applied_jobs = Job.objects.filter(assignee=request.user).select_related('poster').order_by('-created_at')
    
    # Group jobs by client (poster) to get unique clients
    clients_data = {}
    for job in applied_jobs:
        client_id = job.poster.id
        if client_id not in clients_data:
            # Get client profile if available
            client_profile = None
            try:
                client_profile = job.poster.profile
            except:
                pass
            
            clients_data[client_id] = {
                'id': client_id,
                'name': job.poster.get_full_name() or job.poster.username,
                'username': job.poster.username,
                'email': job.poster.email or 'No email',
                'phone': getattr(client_profile, 'phone_number', 'Not provided') if client_profile else 'Not provided',
                'company': getattr(client_profile, 'location', 'Not specified') if client_profile else 'Not specified',
                'photo_url': client_profile.profile_picture.url if client_profile and client_profile.profile_picture else None,
                'jobs': [],
                'projects_count': 0,
            }
        
        # Add job to client's jobs list
        clients_data[client_id]['jobs'].append({
            'id': job.id,
            'title': job.title,
            'status': job.status,
            'status_display': job.get_status_display(),
            'deadline': job.deadline,
            'price': job.price,
            'department': job.department,
        })
        clients_data[client_id]['projects_count'] = len(clients_data[client_id]['jobs'])
    
    # Convert to list for template
    clients_list = list(clients_data.values())
    
    # Calculate statistics
    total_clients = len(clients_list)
    active_clients = len([c for c in clients_list if any(j['status'] in ['IN_PROGRESS', 'POSTED'] for j in c['jobs'])])
    projects_in_progress = len([j for client in clients_list for j in client['jobs'] if j['status'] == 'IN_PROGRESS'])
    
    context = {
        'clients': clients_list,
        'total_clients': total_clients,
        'active_clients': active_clients,
        'projects_in_progress': projects_in_progress,
    }
    
    return render(request, 'users/dashboardfiles/clients.html', context)

#application part...
@login_required
def dashboard(request):
    user = request.user

    # As applicant - counts by status
    stats = Application.objects.filter(applicant=user).values('status').annotate(count=models.Count('id'))
    counts = {'PENDING': 0, 'ACTIVE': 0, 'DECLINED': 0}
    total_applied = 0
    for item in stats:
        counts[item['status']] = item['count']
        total_applied += item['count']

     #dashboard view to supply incoming applications
       
@login_required
def dashboard(request):
    user = request.user
    # Applicant-side: compute counts and list
    my_applications = Application.objects.filter(applicant=user)
    stats = (
        my_applications
        .values('status')
        .annotate(count=models.Count('id'))
    )
    counts = {'PENDING': 0, 'ACTIVE': 0, 'DECLINED': 0}
    total_applied = 0
    for item in stats:
        status_key = item['status']
        # Map model's ACCEPTED to UI's ACTIVE label without changing templates
        if status_key == 'ACCEPTED':
            counts['ACTIVE'] = item['count']
        else:
            counts[status_key] = item['count']
        total_applied += item['count']

    # Creator-side: incoming applications for jobs the user posted
    incoming_applications = Application.objects.filter(job__poster=user).select_related('job', 'applicant')

    context = {
        # preserve both names to avoid template mismatches
        'my_applications': my_applications,
        'your_applications': my_applications,
        'incoming_applications': incoming_applications,
        'application_counts': counts,
        'total_applied': total_applied,
    }

    return render(request, 'users/dashboard.html', context)

    # If user is a creator: list of incoming applications
    incoming_apps = Application.objects.filter(job__poster=user).select_related('job', 'applicant')


    context = {
        # existing context...
        'application_counts': counts,
        'total_applied': total_applied,
        'incoming_applications': incoming_apps,
    }
    return render(request, 'users/dashboard.html', context)