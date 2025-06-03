from django import forms
from .models import Issue


class IssueUpdateForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ["status", "priority"]
        widgets = {
            "status": forms.Select(choices=Issue.STATUS_CHOICES, attrs={'class': 'uk-select'}),
            "priority": forms.Select(choices=Issue.PRIORITY_CHOICES, attrs={'class': 'uk-select'}),
        }


class IssueCreateForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = [
            "title",
            "description",
            "client",
            "priority",
            "department",
            "assigned_to",
            "findings",
            "recommendations",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4, "class": "uk-textarea"}),
            "assigned_to": forms.SelectMultiple(attrs={"class": "select2 uk-select"}),
            "title": forms.TextInput(attrs={"class": "uk-input"}),
            "priority": forms.Select(attrs={"class": "uk-select"}),
            "department": forms.Select(attrs={"class": "select2 uk-select"}),
            "findings": forms.Textarea(attrs={"class": "uk-textarea"}),
            "recommendations": forms.Textarea(attrs={"class": "uk-textarea"}),
            "client": forms.TextInput(attrs={"class": "uk-input"}),
        }
