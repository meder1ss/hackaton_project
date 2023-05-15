from django.db import models
from  django.contrib.auth.models import User


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    PROGRAMMING_LANGUAGES = (
        (1, 'any'),
        (2, 'java'),
        (3, 'c++')
    )
    name = models.CharField(max_length=200)
    description = models.TextField()
    input = models.TextField(null=True, blank=True)
    output = models.TextField()
    try_all = models.IntegerField(default=0)
    try_true = models.IntegerField(default=0)
    language = models.PositiveSmallIntegerField(choices=PROGRAMMING_LANGUAGES, default=1)

    def __str__(self):
        return self.name


class News(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    author = models.CharField(max_length=200)
    time = models.DateTimeField()

    def __str__(self):
        return self.name


class MemberTask(models.Model):
    member_id = models.ForeignKey('Member', on_delete=models.CASCADE, to_field='id', unique=False)
    task_id = models.ForeignKey('Task', on_delete=models.CASCADE, to_field='id', unique=False)
    time = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField()
    code = models.TextField()

    def __str__(self):
        return self.code
