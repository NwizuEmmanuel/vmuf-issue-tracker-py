from django.shortcuts import render, get_object_or_404, redirect
from .models import Issue, Department
from .forms import IssueUpdateForm, IssueCreateForm
from django.template.loader import get_template
import os
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import timezone
from datetime import datetime


# Create your views here.
@login_required
def index(request):
    issues = Issue.objects.filter(created_at__date=timezone.now().date())
    return render(request, "tracker/index.html", {"issues": issues})


@login_required
def update_issue(request, issue_id):
    issue = get_object_or_404(Issue, pk=issue_id)

    if request.method == "POST":
        form = IssueUpdateForm(request.POST, instance=issue)
        if form.is_valid():
            form.save()
            return redirect("index")
    else:
        form = IssueUpdateForm(instance=issue)

    return render(request, "tracker/update_issue.html", {"form": form, "issue": issue})


@login_required
def create_issue(request):
    if request.method == "POST":
        form = IssueCreateForm(request.POST)
        if form.is_valid():
            issue = form.save()
            return redirect("issues")
    else:
        form = IssueCreateForm()
    return render(request, "tracker/create_issue.html", {"form": form})


@login_required
def delete_issue(request):
    if request.method == "POST":
        issue_id = request.POST.get("issue_id")
        issue = get_object_or_404(Issue, pk=issue_id)
        issue.delete()
        return redirect("index")


@login_required
def generate_pdf(request):
    issue_id = None
    issue = None
    if request.method == "POST":
        issue_id = request.POST.get("issue_id")
        issue = get_object_or_404(Issue, pk=issue_id)
        return render(request, 'tracker/issue_pdf.html', {"issue": issue})


from datetime import datetime, time
from django.utils import timezone

@login_required
def issue_filter(request):
    if request.method == 'POST':
        start_date_str = request.POST.get("start_date", "").strip()
        end_date_str = request.POST.get("end_date", "").strip()

        if start_date_str and end_date_str:
            # Parse only the date (no time part)
            start_naive = datetime.strptime(start_date_str, "%Y-%m-%d")
            end_naive = datetime.strptime(end_date_str, "%Y-%m-%d")

            # Add time range to cover full day
            start_naive = datetime.combine(start_naive, time.min)  # 00:00:00
            end_naive = datetime.combine(end_naive, time.max)      # 23:59:59.999999

            # Make aware if USE_TZ = True
            start_date = timezone.make_aware(start_naive)
            end_date = timezone.make_aware(end_naive)

            # Query
            issues = Issue.objects.filter(created_at__range=(start_date, end_date))
            return render(request, "tracker/filter_issues.html", {'issues': issues})

    return render(request, 'tracker/filter_issues.html')
