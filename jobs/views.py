from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime
from decimal import Decimal, InvalidOperation
from .models import Job


@login_required
def job_list(request):
    qs = Job.objects.filter(status=Job.Status.POSTED, is_active=True)
    if request.GET.get('future', '1') == '1':
        qs = qs.filter(deadline__gte=timezone.now().date())
    department = request.GET.get('department')
    if department:
        qs = qs.filter(department__iexact=department)
    context = { 'jobs': qs }
    return render(request, 'jobs/list.html', context)


@login_required
def job_detail(request, pk: int):
    job = get_object_or_404(Job, pk=pk)
    return render(request, 'jobs/detail.html', { 'job': job })


@login_required
def create_job(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        department = request.POST.get('department')
        unit = request.POST.get('unit', '').strip()
        price_raw = request.POST.get('price')
        deadline_raw = request.POST.get('deadline')
        description = request.POST.get('description') or ''

        if not title or not department or not price_raw or not deadline_raw:
            return render(request, 'jobs/create_assigment.html', {
                'error': 'Please fill in all required fields.',
                'form': request.POST,
            })

        try:
            price = Decimal(str(price_raw))
        except (TypeError, ValueError, InvalidOperation):
            return render(request, 'jobs/create_assigment.html', {
                'error': 'Price must be a valid number.',
                'form': request.POST,
            })

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
        return redirect('jobs:list')

    return render(request, 'jobs/create_assigment.html')

