from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


from django.core.exceptions import ValidationError

class Level(models.Model):

    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(null=True, blank=True, max_length=87)
    created = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=True)
    slug = models.SlugField(max_length=250, unique=True, null=True, blank=True)
    icon = models.CharField(max_length=100, default='circle', editable=True, null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Level, self).save(*args, **kwargs)

class VocabLevel(models.Model):

    level = models.ForeignKey(Level, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=250, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    example = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class UserLevel(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    favorite = models.BooleanField(default=False)
    progress = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.level, self.user.username

def content_file_name(instance, filename):
    return "sounds/{instance}/{file}".format(instance=instance.level, file=filename)

class Question(models.Model):

    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    name = models.CharField(max_length=700)
    approved = models.BooleanField(default=True)
    robot_voice = models.FileField(upload_to=content_file_name, blank=True, null=True)

    def __str__(self):
        return self.name

class ClickCounter(models.Model):

    button = models.CharField(max_length=250, blank=True, null=True)
    counter = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return '{} {}'.format(self.button, self.counter)

class AppFile(models.Model):

    title = models.CharField(max_length=250)
    platform = models.CharField(max_length=20, blank=True, null=True)
    file = models.FileField(upload_to='app_files/', blank=True, null=True)
    count = models.PositiveIntegerField(default=0, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    update = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:

        ordering = ['-created']
