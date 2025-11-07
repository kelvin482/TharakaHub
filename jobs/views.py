from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseForbidden
from datetime import datetime
from decimal import Decimal, InvalidOperation

from .models import Job, Application


# =======================
# JOB LIST VIEW
# =======================
@login_required
def job_list(request):
    """List all active jobs available for application."""
    qs = Job.objects.filter(status=Job.Status.POSTED, is_active=True)

    # Show only jobs with deadlines in the future
    if request.GET.get('future', '1') == '1':
        qs = qs.filter(deadline__gte=timezone.now().date())

    # Filter by department if provided
    department = request.GET.get('department')
    if department:
        qs = qs.filter(department__iexact=department)

    context = {'jobs': qs}
    return render(request, 'jobs/list.html', context)


# =======================
# JOB DETAIL VIEW
# =======================
@login_required
def job_detail(request, pk: int):
    """Show detailed information about a job."""
    job = get_object_or_404(Job, pk=pk)

    # If job poster is viewing, show applications for that job
    applications = None
    if request.user == job.poster:
        applications = job.applications.all()

    context = {
        'job': job,
        'applications': applications,
    }
    return render(request, 'jobs/detail.html', context)


# =======================
# CREATE NEW JOB
# =======================
@login_required
def create_job(request):
    """Allow a user to create a new job posting."""
    if request.method == 'POST':
        title = request.POST.get('title')
        department = request.POST.get('department')
        unit = request.POST.get('unit', '').strip()
        price_raw = request.POST.get('price')
        deadline_raw = request.POST.get('deadline')
        description = request.POST.get('description') or ''

        # Validate required fields
        if not title or not department or not price_raw or not deadline_raw:
            return render(request, 'jobs/create_assigment.html', {
                'error': 'Please fill in all required fields.',
                'form': request.POST,
            })

        # Validate price
        try:
            price = Decimal(str(price_raw))
        except (TypeError, ValueError, InvalidOperation):
            return render(request, 'jobs/create_assigment.html', {
                'error': 'Price must be a valid number.',
                'form': request.POST,
            })

        # Validate deadline
        try:
            raw = deadline_raw.strip()
            if 'T' in raw:
                raw = raw.split('T', 1)[0]
            deadline = datetime.strptime(raw, '%Y-%m-%d').date()
        except ValueError:
            return render(request, 'jobs/create_assigment.html', {
                'error': 'Deadline must be a valid date (YYYY-MM-DD).',
                'form': request.POST,
            })

        if deadline < timezone.now().date():
            return render(request, 'jobs/create_assigment.html', {
                'error': 'Deadline cannot be in the past.',
                'form': request.POST,
            })

        # Create job
        Job.objects.create(
            poster=request.user,
            title=title,
            description=description,
            department=department,
            unit=unit,
            price=price,
            deadline=deadline,
            status=Job.Status.POSTED,
        )

        messages.success(request, "Job created successfully.")
        return redirect('jobs:list')

    return render(request, 'jobs/create_assigment.html')


# =======================
# APPLY FOR A JOB
# =======================
@login_required
def apply_job(request, job_id):
    """Allow a user to apply for a job."""
    job = get_object_or_404(Job, id=job_id)

    # Prevent job creator from applying
    if job.poster == request.user:
        messages.error(request, "You cannot apply to your own job.")
        return redirect(reverse('jobs:detail', kwargs={'pk': job.id}))

    # Only allow POST requests
    if request.method != 'POST':
        return redirect(reverse('jobs:detail', kwargs={'pk': job.id}))

    cover_letter = request.POST.get('cover_letter', '').strip()

    # Prevent duplicate applications
    application, created = Application.objects.get_or_create(
        job=job,
        applicant=request.user,
        defaults={'cover_letter': cover_letter}
    )

    if not created:
        messages.info(request, "You have already applied to this job.")
        return redirect(reverse('jobs:detail', kwargs={'pk': job.id}))

    # Optional: create notification if Notification model exists
    try:
        from users.models import Notification
        Notification.objects.create(
            recipient=job.poster,
            actor=request.user,
            verb=f"applied to your job '{job.title}'",
            target_job=job
        )
    except Exception:
        pass

    messages.success(request, "Application submitted successfully.")
    return redirect(reverse('jobs:detail', kwargs={'pk': job.id}))


# =======================
# CHANGE APPLICATION STATUS
# =======================
@login_required
def change_application_status(request, app_id, new_status):
    """
    Allow the job creator to accept or decline a job application.
    """
    application = get_object_or_404(Application, id=app_id)

    # Only the job poster can perform this action
    if request.user != application.job.poster:
        return HttpResponseForbidden("You are not allowed to perform this action.")

    # Define valid statuses (assuming your model uses constants)
    valid_statuses = ['ACCEPTED', 'DECLINED', 'PENDING']
    if new_status not in valid_statuses:
        messages.error(request, "Invalid status provided.")
        return redirect('users:dashboard')

    # Update application status
    application.status = new_status
    application.save()

    # Optional: create notification
    try:
        from users.models import Notification
        Notification.objects.create(
            recipient=application.applicant,
            actor=request.user,
            verb=f"Your application for '{application.job.title}' was {new_status.lower()}",
            target_job=application.job
        )
    except Exception:
        pass

    # Feedback message
    messages.success(request, f"Application {new_status.lower()} successfully.")
    return redirect('users:dashboard')
