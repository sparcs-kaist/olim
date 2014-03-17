from django.db import models

class Filesys(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField()
    date = models.DateField(auto_now=True)
    #uploader = models.ForeignKey('account.User')
    thumbnail = models.FileField(upload_to='thumb')

    parent_dir = models.CharField(max_length=100)
    is_dir = models.BooleanField()

    def __str__(self):
        if is_dir:
            return '/' + name
        else:
            return name
