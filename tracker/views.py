from django.shortcuts import render, get_object_or_404, redirect
from .models import Issue
from .forms import IssueUpdateForm

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