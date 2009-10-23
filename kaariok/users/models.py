from django.db import models
from django.contrib.auth.models import User
from kaariok.songs.models import Song

class Rating(models.Model):
    """(Rating description)"""
    KNOWN_VALUES=(
        ('unknown', 'Unknown'),
        ('yes', 'Yes'),
        ('no', 'No'),
        ('love', 'Love'),
    )
    user = models.ForeignKey(User)
    song = models.ForeignKey(Song)
    comment = models.CharField(blank=True, max_length=600)
    value = models.CharField(blank=True, max_length=100)
    # known = models.IntegerField(blank=False, choices=KNOWN_VALUES)


    def __unicode__(self):
        return u"Rating"

