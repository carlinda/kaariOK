from django.db import models

from kaariok.songs.models import Song
from django.contrib.auth.models import User
import datetime


class Playlist(models.Model):
    """(Playlist description)"""
    name = models.TextField(blank=True)
    user = models.ForeignKey(User, blank=True, null=True, unique=True)
    last_accessed = models.DateTimeField(blank=False, default=datetime.datetime.now)

    def __unicode__(self):
        return self.name
    
    @staticmethod
    def get_or_create(user_id):
        try:
            playlist = Playlist.objects.get(user__id=user_id)
            return playlist
        except:
            the_user = User.objects.get(id=user_id)
            playlist = Playlist(name=the_user.username+"'s Playlist", user=the_user)
            playlist.save()
            return playlist

class PlaylistItem(models.Model):
    """(PlaylistItem description)"""
    song = models.ForeignKey(Song)
    playlist = models.ForeignKey(Playlist)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return u"PlaylistItem"
