from django.shortcuts import render, get_object_or_404, redirect
from .models import Issue
from .forms import IssueUpdateForm, IssueCreateForm

# Create your views here.
def index(request):
    issues = Issue.objects.exclude(status='R')
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
            form.save()
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