from django.db import models

from kaariok.songs.models import Song
from django.contrib.auth.models import User
import datetime
from django.db.models import Count


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
    @staticmethod
    def get_or_create_master_playlist():
        try:
            playlist = Playlist.objects.get(name="master")
            return playlist
        except:
            playlist = Playlist(name="master", user=None)
            playlist.save()
            return playlist
    
    @staticmethod
    def get_next_master_item():
        master = Playlist.objects.get(name="master")
        try:
            item = master.playlistitem_set.filter(active=True).order_by('position')[0]
        except:
            item = None
        if item is None:
            # This next query is split into two lines. Tecnically it should compose and execute only when requireing the data
            try:
                item = Playlist.objects.filter(user__is_active=True).annotate(num_items=Count('playlistitem'))
                item = item.filter(num_items__gt=0).order_by('last_accessed')[0].get_next_item()
            except:
                item = None
        return item
    
    def add_song(self, song):
        item = PlaylistItem(song=song, playlist=self, position=-1)
        numberOfItems = self.playlistitem_set.all().count()
        if numberOfItems == 0:
            item.position = 0
        else:
            # Get largest position
            maximum = PlaylistItem.objects.filter(playlist=self, active=True).order_by('-position')[0].position
            item.position = maximum+1
        item.save()
    
    def add_item(self, item):
        numberOfItems = self.playlistitem_set.all().count()
        if numberOfItems == 0:
            item.position = 0
        else:
            # Get largest position
            maximum = PlaylistItem.objects.filter(playlist=self, active=True).order_by('-position')[0].position
            item.position = maximum+1
        item.playlist = self
        item.save()
            
    def remove_item(self, item):
        if item is not None:
            item.delete()
        
    def contains_song(self, song_id):
        song = Song.objects.get(id=song_id)
        number_of_songs = PlaylistItem.objects.filter(playlist=self, song=song, active=True).count()
        if number_of_songs >0:
            return True
        return False
        
    #This returns the first song in the playlist
    def get_next_item(self):
        try:
            return self.playlistitem_set.filter(active=True).order_by('position')[0]
        except:
            return None
    

class PlaylistItem(models.Model):
    """(PlaylistItem description)"""
    song = models.ForeignKey(Song, blank=False, null=True)
    playlist = models.ForeignKey(Playlist)
    active = models.BooleanField(default=True)
    position = models.DecimalField(max_digits=8, decimal_places=6, blank=False, null=False)
    
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
    
    def move_up(self):
        above_me = self.get_item_above_me()
        if above_me is None:
            return
        
        above_me_times_2 = above_me.get_item_above_me()
        if above_me_times_2 is None:
            if above_me.position == 0:
                above_me.position = self.position/2
                above_me.save()
                self.position = 0
                self.save()
                return
            else:
                self.position = above_me.position/2
                self.save()
                return
        
        self.position = (above_me_times_2.position + above_me.position )/2
        self.save()
        return

    def move_down(self):
        below_me = self.get_item_below_me()
        if below_me is None:
            return

        below_me_times_2 = below_me.get_item_below_me()
        if below_me_times_2 is None:
            self.position = below_me.position+1
            self.save()
            return

        self.position = (below_me_times_2.position + below_me.position )/2
        self.save()
        return
            
            
