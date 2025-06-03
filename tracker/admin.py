from django.contrib import admin
from .models import Issue, Department, Professional, Building

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
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs

admin.site.register(Issue, IssueAdmin)
admin.site.register(Department)
admin.site.register(Professional)
admin.site.register(Building)

