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
from django.views.generic import TemplateView


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
class IssueFilterView(TemplateView):
    template_name = 'issues/filter_issues.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        issues = Issue.objects.all()
        departments = Department.objects.all()

        # Get filter parameters from GET request
        month = self.request.GET.get('month')
        date = self.request.GET.get('date')
        title = self.request.GET.get('title', '').strip()
        department = self.request.GET.get('department', '').strip()
        client = self.request.GET.get('client', '').strip()

        # Filter by month (expects 'YYYY-MM')
        if month:
            year, month_num = month.split('-')
            issues = issues.filter(created_at__year=year, created_at__month=month_num)

        # Filter by exact date (expects 'YYYY-MM-DD')
        if date:
            issues = issues.filter(created_at__date=date)

        # Filter by title
        if title:
            issues = issues.filter(title__icontains=title)

        # Filter by department (assuming a ForeignKey named 'department')
        if department:
            issues = issues.filter(department__department_name__iexact=department)

        # Filter by client
        if client:
            issues = issues.filter(client__icontains=client)

        context['issues'] = issues
        context['departments'] = departments
        context['today'] = timezone.now().date().isoformat()
        return context

