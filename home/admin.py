from django.contrib import admin
from django.http import HttpResponseRedirect
from .models import Issue, Department, Staff, Building
from django.utils.translation import gettext_lazy as _
from django.urls import path, reverse
from django.contrib import messages

class MonthFilter(admin.SimpleListFilter):
    title = 'month'
    parameter_name = 'month'
    
    def lookups(self, request, model_admin):
        return (
            ('1', 'January'),
            ('2', 'February'),
            ('3', 'March'),
            ('4', 'April'),
            ('5', 'May'),
            ('6', 'June'),
            ('7', 'July'),
            ('8', 'August'),
            ('9', 'September'),
            ('10', 'October'),
            ('11', 'November'),
            ('12', 'December'),
        )
        
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(created_at__month=self.value())
        return queryset
    
class IssueAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'priority', 'created_at', 'updated_at')
    list_filter = (MonthFilter, 'assigned_to', 'created_at', 'status', 'priority')
    date_hierarchy = 'created_at'
    actions = ['print_selected']
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('print/', self.admin_site.admin_view(self.print_view), name='mymodel_print'),
        ]
        return custom_urls + urls
    
    def print_selected(self, request, queryset):
        selected = queryset.values_list('pk', flat=True)
        
        if queryset.count() > 2:
            self.message_user(
                request,
                "You can only print up to 2 items at a time.",
                level=messages.ERROR
            )
            return HttpResponseRedirect(request.get_full_path())
        
        return HttpResponseRedirect(
            reverse('admin:mymodel_print') + f"?ids={','.join(str(pk) for pk in selected)}"
        )
    print_selected.short_description = "Print selected items"
    
    def print_view(self, request):
        from django.shortcuts import render
        ids = request.GET.get("ids", "")
        id_list = ids.split(",") if ids else []
        objects = Issue.objects.filter(id__in=id_list)
        return render(request, "printing/print_selected.html", {"objects": objects})
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs

admin.site.register(Issue, IssueAdmin)
admin.site.register(Department)
admin.site.register(Staff)
admin.site.register(Building)

admin.site.site_header = _("VMUF Issue Tracker")
admin.site.site_title = _("VMUF Admin")
admin.site.index_title = _("Dashboard")