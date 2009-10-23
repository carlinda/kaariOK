from django.db import models

class Language(models.Model):
    """(Language description)"""
    short = models.CharField(blank=False, max_length=2)
    full = models.CharField(blank=False, max_length=100)    

    def __unicode__(self):
        return u"Language"


class Album(models.Model):
    """(Album description)"""
    code = models.CharField(blank=False, max_length=100)

    def __unicode__(self):
        return self.code


class Artist(models.Model):
    """(Artist description)"""
    name = models.CharField(blank=False, max_length=200)

    def __unicode__(self):
        return self.name


class Song(models.Model):
    """(Song description)"""
    APPROVAL_CHOICES = (
        (0, "Doesn't know"),
        (1, "Yes"),
        (2, "No"),
    )
    artist = models.ForeignKey(Artist)
    album = models.ForeignKey(Album)
    name = models.CharField(blank=False, max_length=300)
    track = models.IntegerField(blank=True, null=True)
    approved = models.IntegerField(blank=False, null=False, choices=APPROVAL_CHOICES)
    filename = models.CharField(blank=False, max_length=300)
    language = models.ForeignKey(Language)

    def __unicode__(self):
        return self.name

