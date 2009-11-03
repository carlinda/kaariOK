from django.db import models
from django.contrib.auth.models import User
from kaariok.songs.models import Song


class Rating(models.Model):
    """(Rating description)"""
    KNOWN_VALUES=(
        ('meh', 'Meh'),
        ('known', 'Known'),
        ('hate', 'Hate'),
        ('love', 'Love'),
    )
    user = models.ForeignKey(User)
    song = models.ForeignKey(Song)
    comment = models.CharField(blank=True, max_length=600)
    value = models.CharField(blank=False, choices=KNOWN_VALUES, max_length=7)

    def __unicode__(self):
        return u"Rating"

