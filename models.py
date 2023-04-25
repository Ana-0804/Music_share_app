from django.db import models
from django.contrib.auth.models import User

class MusicFile(models.Model):
    PUBLIC = 'public'
    PRIVATE = 'private'
    PROTECTED = 'protected'
    MUSIC_FILE_TYPES = [
        (PUBLIC, 'Public'),
        (PRIVATE, 'Private'),
        (PROTECTED, 'Protected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='music/')
    type = models.CharField(max_length=20, choices=MUSIC_FILE_TYPES, default=PUBLIC)
    allowed_users = models.ManyToManyField(User, related_name='allowed_music_files', blank=True)

    def __str__(self):
        return self.title
