from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import JobForm, ProposalForm
from .models import MarketingJob, Proposal, Category
from .services.ai import classify_job_text


def jobs_list(request):
    qs = MarketingJob.objects.filter(status=MarketingJob.STATUS_OPEN)

    q = request.GET.get('q', '').strip()
    if q:
        qs = qs.filter(
            Q(title__icontains=q) |
            Q(tags__icontains=q) |
            Q(description__icontains=q)
        )

    cat_slug = request.GET.get('category')
    current_category = None
    if cat_slug:
        current_category = get_object_or_404(Category, slug=cat_slug)
        qs = qs.filter(category=current_category)

    paginator = Paginator(qs, 12)
    page = request.GET.get('page')
    jobs = paginator.get_page(page)

    # ✅ Prepare tag list for each job
    for job in jobs:
        if job.tags:
            job.tag_list = [t.strip() for t in job.tags.split(",") if t.strip()]
        else:
            job.tag_list = []

    ctx = {
        'jobs': jobs,
        'q': q,
        'categories': Category.objects.all(),
        'current_category': current_category,
    }
    return render(request, 'marketing/jobs_list.html', ctx)


@login_required
def job_create(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job: MarketingJob = form.save(commit=False)
            job.poster = request.user

            # ✅ AI Category Suggestion
            job.ai_category_suggestion = classify_job_text(job.description)

            job.save()
            return redirect('marketing:job_detail', pk=job.pk)
    else:
        form = JobForm()

    return render(request, 'marketing/job_form.html', {'form': form})


def job_detail(request, pk: int):
    job = get_object_or_404(MarketingJob, pk=pk)

    # ✅ Prepare tag list
    if job.tags:
        job.tag_list = [t.strip() for t in job.tags.split(",") if t.strip()]
    else:
        job.tag_list = []

    proposal_form = None
    proposals = None

    if request.user.is_authenticated:
        if request.user == job.poster:
            proposals = job.proposals.select_related('provider').all()
        else:
            # Check if this user already submitted a proposal
            if not Proposal.objects.filter(job=job, provider=request.user).exists():
                proposal_form = ProposalForm()

    ctx = {
        'job': job,
        'proposals': proposals,
        'proposal_form': proposal_form,
    }
    return render(request, 'marketing/job_detail.html', ctx)


@login_required
def proposal_create(request, pk: int):
    job = get_object_or_404(MarketingJob, pk=pk)

    if request.method != 'POST':
        raise Http404()

    form = ProposalForm(request.POST)
    if form.is_valid():
        proposal: Proposal = form.save(commit=False)
        proposal.job = job
        proposal.provider = request.user

        try:
            proposal.save()
        except Exception as e:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'ok': False, 'errors': str(e)}, status=400)
            return redirect('marketing:job_detail', pk=job.pk)

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'ok': True, 'proposal_id': proposal.pk})

        return redirect('marketing:job_detail', pk=job.pk)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'ok': False, 'errors': form.errors.as_json()}, status=400)

    return redirect('marketing:job_detail', pk=job.pk)


@login_required
def dashboard(request):
    posted_jobs = MarketingJob.objects.filter(
        poster=request.user
    ).order_by('-created_at')

    proposals_made = Proposal.objects.filter(
        provider=request.user
    ).select_related('job').order_by('-created_at')

    return render(request, 'marketing/dashboard.html', {
        'posted_jobs': posted_jobs,
        'proposals_made': proposals_made,
    })
