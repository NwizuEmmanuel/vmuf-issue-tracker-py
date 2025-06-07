from django.db import models
from django.db.models import Max
from django.utils import timezone

# Create your models here.
class Building(models.Model):
    building_fullname = models.CharField(max_length=200)
    building_short_name = models.CharField(max_length=20)

    def __str__(self):
        return self.building_short_name


class Department(models.Model):
    department_name = models.CharField(max_length=200)
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name="departments")
    local_number = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ["department_name", "building"]
    
    def __str__(self):
        return f"{self.department_name}"

class Professional(models.Model):
    fullname = models.CharField(max_length=200)
    specialty = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.fullname}"
    
class Issue(models.Model):
    PRIORITY_CHOICES = [
        ('L', 'Low'),
        ('M', 'Medium'),
        ('H', 'High'),
    ]
    
    STATUS_CHOICES = [
        ('O', 'Open'),
        ('A', 'Assigned'),
        ('P', 'In Progress'),
        ('R', 'Resolved'),
        ('C', 'Cancelled'),
    ]
    
    issue_number = models.CharField(max_length=20, unique=True, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField()
    findings = models.TextField(null=True, blank=True)
    recommendations = models.TextField(null=True, blank=True)
    client = models.CharField(max_length=200)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="issues")
    assigned_to = models.ManyToManyField(Professional, blank=True, related_name="assigned_issues")
    priority = models.CharField(
        max_length=1,
        choices=PRIORITY_CHOICES,
        default='M'
    )
    
    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default='O'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.issue_number} - {self.title} ({self.get_status_display()})"
    
    def save(self, *args, **kwargs):
        if not self.issue_number:
            today = timezone.now().date()
            date_part = today.strftime("%Y%m%d")
            
            # Get department prefix (First 3 letters)
            dept_prefix = self.department.department_name[:3].upper()
            
            last_issue = Issue.objects.filter(
                issue_number__startswith=f"{dept_prefix}-{date_part}"
            ).aggregate(Max('issue_number'))
            
            if last_issue['issue_number__max']:
                last_seq = int(last_issue['issue_number__max'].split('-')[-1])
                new_seq = last_seq + 1
            else:
                new_seq = 1
                
            self.issue_number = f"{dept_prefix}-{date_part}-{new_seq:03d}"
        super().save(*args, **kwargs)