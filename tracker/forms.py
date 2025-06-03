from django import forms
from .models import Issue

class IssueUpdateForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['status', 'priority']
        widgets = {
            'status': forms.Select(choices=Issue.STATUS_CHOICES),
            'priority': forms.Select(choices=Issue.PRIORITY_CHOICES)
        }