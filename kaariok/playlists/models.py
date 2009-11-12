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
    
    def add_song(self, song):
        item = PlaylistItem(song=song, playlist=self, position=-1)
        numberOfItems = self.playlistitem_set.all().count()
        if numberOfItems == 0:
            item.position = 0
        else:
            # Get largest position
            maximum = PlaylistItem.objects.filter(playlist=self).order_by('-position')[0].position
            item.position = maximum+1
        item.save()
        
    def remove_song(self, song):
        item = PlaylistItem.objects.get(song=song, playlist=self, active=True)
        
        if item is not None:
            item.delete()
        
    def contains_song(self, song_id):
        song = Song.objects.get(id=song_id)
        number_of_songs = PlaylistItem.objects.filter(playlist=self, song=song, active=True).count()
        if number_of_songs >0:
            return True
        return False

class PlaylistItem(models.Model):
    """(PlaylistItem description)"""
    song = models.ForeignKey(Song, blank=False, null=True)
    playlist = models.ForeignKey(Playlist)
    active = models.BooleanField(default=True)
    position = models.IntegerField(blank=False, null=False)
    
    def __unicode__(self):
        return self.song.name + " on " + self.playlist.name
        
    def get_item_above_me(self):
        try:
            return PlaylistItem.objects.filter(playlist=self.playlist, active=True, position__lt=self.position).order_by('-position')[0]
        except:
            return None
    
    def get_item_below_me(self):
        try:
            return PlaylistItem.objects.filter(playlist=self.playlist, active=True, position__gt=self.position).order_by('position')[0]
        except:
            return None        
