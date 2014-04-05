from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from django.conf import settings

fs = FileSystemStorage(location=settings.PROJECT_DIR, base_url='/')

class Filesys(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=200, unique=True, db_index=True)
    format = models.CharField(max_length=10)
    date = models.DateField(auto_now=True)
    uploader = models.ForeignKey(User, null=True, blank=True)
    file = models.FileField(storage=fs, upload_to='files', null=True, blank=True)
    thumbnail = models.FileField(upload_to='thumbs', null=True, blank=True)
    parent_dir = models.IntegerField(null=True, blank=True)
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
