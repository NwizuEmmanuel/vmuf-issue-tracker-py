from django.db import models

# Create your models here.
class Building(models.Model):
    building_fullname = models.CharField(max_length=200)
    building_short_name = models.CharField(max_length=20)

    def __str__(self):
        return self.building_short_name


class Departments(models.Model):
    department_name = models.CharField(max_length=200)
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name="departments")
    local_number = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ["department_name", "building"]
    
    def __str__(self):
        return f"{self.department_name} (Building: {self.building.building_short_name})"

class Professionals(models.Model):
    fullname = models.CharField(max_length=200)
    specialty = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.fullname} (Role: {self.specialty})"
    
class Issues(models.Model):
    PRIORTY_CHOICES = [
        ('L', 'Low'),
        ('M', 'Medium'),
        ('H', 'High'),
    ]
    
    STATUS_CHOICES = [
        ('O', 'Open'),
        ('A', 'Assigned'),
        ('P', 'In Progress'),
        ('R', 'Resolved'),
    ]
    
    issue_number = models.CharField(max_length=20, unique=True, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField()
    client = models.CharField(max_length=200)
    department = models.ForeignKey(Departments, on_delete=models.CASCADE, related_name="issues")
    assigned_to = models.ForeignKey(Professionals, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_issues")
    priorty = models.CharField(
        max_length=1,
        choices=PRIORTY_CHOICES,
        default='M'
    )
    
    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default='O'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)