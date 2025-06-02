from django.shortcuts import render
from .models import Issue

# Create your views here.
def index(request):
    issues = Issue.objects.exclude(status='R')
    return render(request, "index.html", {"issues": issues})