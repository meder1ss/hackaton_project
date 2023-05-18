from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    PROGRAMMING_LANGUAGES = (
        (1, 'any'),
        (2, 'python'),
        (3, 'ruby')
    )
    name = models.CharField(max_length=200)
    description = models.TextField()
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


class UserTask(models.Model):
    PROGRAMMING_LANGUAGES = (
        (1, 'python'),
        (2, 'ruby')
    )
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, to_field='id', unique=False)
    task_id = models.ForeignKey('Task', on_delete=models.CASCADE, to_field='id', unique=False)
    time = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField()
    code = models.TextField()
    language = models.PositiveSmallIntegerField(choices=PROGRAMMING_LANGUAGES, default=2)

    def __str__(self):
        return self.code
