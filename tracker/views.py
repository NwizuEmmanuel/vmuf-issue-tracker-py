from django.shortcuts import render, get_object_or_404, redirect
from .models import Issue, Department
from .forms import IssueUpdateForm, IssueCreateForm
from django.template.loader import get_template
from weasyprint import HTML, CSS
import os
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import timezone
from datetime import date


# Create your views here.
@login_required
def index(request):
    issues = Issue.objects.filter(created_at__date=timezone.now().date())
    return render(request, "issues/index.html", {"issues": issues})


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

    return render(request, "issues/update_issue.html", {"form": form, "issue": issue})


@login_required
def create_issue(request):
    if request.method == "POST":
        form = IssueCreateForm(request.POST)
        if form.is_valid():
            issue = form.save()
            return redirect("issues")
    else:
        form = IssueCreateForm()
    return render(request, "issues/create_issue.html", {"form": form})


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

    template = get_template("issues/issue_pdf.html")
    html_string = template.render({"issue": issue})

    html = HTML(string=html_string, base_url=request.build_absolute_uri("/"))
    # css_path = os.path.join(settings.STATICFILES_DIRS[0], 'css', 'uikit.min.css')

    # css = CSS(filename=css_path)

    pdf_file = html.write_pdf(stylesheet=[])
    response = HttpResponse(pdf_file, content_type="application/pdf")
    return response


@login_required
def bulk_print_issue(request):
    departments = Department.objects.all()
    issues = None
    timenow = date.today().isoformat()  # Use date.today() for a date string

    if request.method == "POST":
        start_date = request.POST.get("start_date", "").strip()
        end_date = request.POST.get("end_date", "").strip()
        title = request.POST.get("title", "").strip()
        client = request.POST.get("client", "").strip()

        # Only filter if all fields are provided
        if start_date and end_date and title and client:
            issues = Issue.objects.filter(
                created_at__date__range=(start_date, end_date),
                title=title,
                client=client,
            )
        else:
            issues = Issue.objects.none()  # Or handle missing fields as needed

        return render(
            request,
            "issues/bulk_print.html",
            {"departments": departments, "issues": issues, "timenow": timenow},
        )

    return render(
        request,
        "issues/bulk_print.html",
        {"departments": departments, "timenow": timenow},
    )
