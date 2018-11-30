from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Members(models.Model):

    name = models.CharField(max_length=100)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class StitchBoard(models.Model):
    title = models.CharField(max_length=100)
    user = models.ForeignKey(User, related_name='StitchBoards',
                             on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Label(models.Model):
    board = models.ForeignKey(StitchBoard, related_name='Labels',
                              on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class StitchList(models.Model):
    board = models.ForeignKey(StitchBoard, related_name='StitchLists',
                              on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class StitchCard(models.Model):
    list = models.ForeignKey(StitchList, related_name='StitchCards',
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    DueDate = models.DateField()
    # Label = models.CharField(max_length=50)
    active = models.BooleanField(default=True)
    member = models.ForeignKey(Members, related_name='StitchCards',
                               on_delete=models.CASCADE, default=1)
    labels = models.ForeignKey(Label, related_name='StitchCards',
                               on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.title
