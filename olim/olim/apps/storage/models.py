from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.core.exceptions import ValidationError

class Filesys(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    format = models.CharField(max_length=20)
    date = models.DateField(auto_now=True)
    uploader = models.ForeignKey(User)
    thumbnail = models.FileField(upload_to='thumb', null=True, blank=True)

    parent_dir = models.CharField(max_length=100, null=True, blank=True)
    is_dir = models.BooleanField(default=False)
    is_secured = models.BooleanField(default=False)

    def __unicode__(self):
        if self.is_dir:
            return '/' + u'%s' % (self.name)
        else:
            return u'%s' % (self.name)

    def clean(self):
        if self.name.find('/') > -1:
            raise ValidationError('You must not contain / character.')

# Admin

class FilesysAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'date', 'uploader', 'thumbnail', 'parent_dir', 'is_dir')
    ordering = ('is_dir', 'name')

admin.site.register(Filesys, FilesysAdmin)
