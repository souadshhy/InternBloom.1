from django.db import models
from django.contrib.auth.models import User

# define choices
APPLICATION_STATUS = [
    ('pending', 'Pending'),
    ('accepted', 'Accepted'),
    ('rejected', 'Rejected'),
]
SECTOR = [
    ('private', 'Private'),
    ('public', 'Public'),
]


class Depart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    deptName = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.deptName


class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    department = models.ForeignKey(Depart, on_delete=models.PROTECT)
    major = models.CharField(max_length=100)
    year = models.DateField()

    def __str__(self):
        return f"{self.name} {self.surname}"


class Company(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    companyName = models.CharField(max_length=100, unique=True)
    sector = models.CharField(max_length=20, choices=SECTOR, default='public')
    industry = models.CharField(max_length=100)

    def __str__(self):
        return self.companyName


class Position(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    duration = models.PositiveIntegerField()  # in months
    location = models.CharField(max_length=100)
    paid = models.BooleanField()
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title}"


class Apps(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    appStatus = models.CharField(
        max_length=10,
        choices=APPLICATION_STATUS,
        default='pending'
    )
    appliedDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student}'s Application"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the current application

        if self.appStatus == 'accepted':
            # 1. Mark position as unavailable
            self.position.available = False
            self.position.save()

            # 2. Reject all other apps for this position
            Apps.objects.filter(
                position=self.position
            ).exclude(id=self.id).update(appStatus='rejected')

    class Meta:
        ordering = ['student']
