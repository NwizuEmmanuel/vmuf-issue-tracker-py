from django.shortcuts import render, get_object_or_404, redirect
from .models import Issue
from .forms import IssueUpdateForm, IssueCreateForm
from django.template.loader import get_template
from weasyprint import HTML, CSS
import os
from django.conf import settings
from django.http import HttpResponse

# Create your views here.
def index(request):
    issues = Issue.objects.exclude(status='R').exclude(status="C")
    return render(request, "issues/index.html", {"issues": issues})

def update_issue(request, issue_id):
    issue = get_object_or_404(Issue, pk=issue_id)
    
    if request.method == 'POST':
        form = IssueUpdateForm(request.POST, instance=issue)
        if form.is_valid():
            form.save()
            return redirect("index")
    else:
        form = IssueUpdateForm(instance=issue)
    
    return render(request, 'issues/update_issue.html', {
        'form': form,
        'issue': issue
    })

def create_issue(request):
    if request.method == 'POST':
        form = IssueCreateForm(request.POST)
        if form.is_valid():
            issue = form.save()
            return redirect("issues")
    else:
        form = IssueCreateForm()
    return render(request, "issues/create_issue.html", {'form': form})

def delete_issue(request):    
    if request.method == "POST":
        issue_id = request.POST.get("issue_id")
        issue = get_object_or_404(Issue, pk=issue_id)
        issue.delete()
        return redirect("index")

def generate_pdf(request):
    template = get_template("issue_form.html")
    html_string = template.render({})
    
    html = HTML(string=html_string, base_url=request.build_absolute_uri('/'))
    css_path = os.path.join(settings.STATIC_ROOT, 'css', 'pdf.csss')
    
    css = CSS(filename=css_path)
    
    pdf_file = html.write_pdf(stylesheet=[css])
    response = HttpResponse(pdf_file, content_type='application/pdf')
    return response