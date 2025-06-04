from django import forms
from .models import Issue


class IssueUpdateForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = [
            "department",
            "client",
            "title",
            "description",
            "assigned_to",
            "findings",
            "recommendations",
            "priority",
            "status",
        ]
        widgets = {
            "department": forms.Select(attrs={"class": "select2 uk-select"}),
            "client": forms.TextInput(attrs={"class": "uk-input"}),
            "title": forms.TextInput(attrs={"class": "uk-input"}),
            "description": forms.Textarea(attrs={"rows": 4, "class": "uk-textarea"}),
            "assigned_to": forms.SelectMultiple(attrs={"class": "select2 uk-select"}),
            "findings": forms.Textarea(attrs={"class": "uk-textarea"}),
            "recommendations": forms.Textarea(attrs={"class": "uk-textarea"}),
            "priority": forms.Select(
                choices=Issue.PRIORITY_CHOICES, attrs={"class": "uk-select"}
            ),
            "status": forms.Select(
                choices=Issue.STATUS_CHOICES, attrs={"class": "uk-select"}
            ),
        }


class IssueCreateForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = [
            "department",
            "client",
            "title",
            "description",
            "assigned_to",
            "findings",
            "recommendations",
            "priority",
            "status",
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
            "status": forms.Select(attrs={"class": "uk-select"}),
        }
