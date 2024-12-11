import models
from collections import defaultdict

#this class will contain the top songs for all the genres that a user's query relates to
class TopSongs:
    def __init__(self,genre:list,num_songs:int = 5):
        self.genre = genre
        self.num_songs = num_songs
        self.results = defaultdict()

    #this function is to return the dictionary of every single song:artist pair that we have extracted from every genre
    def get_all_top_songs(self) -> defaultdict:
        for g in self.genre:
            self.results.update(self.get_tracks_by_genre(g))
        return self.results
            
    def get_tracks_by_genre(self,genre:str)-> defaultdict: 
        results = models.sp.search(q=f"genre:{genre}", type="track", limit=self.num_songs)
        tracks = defaultdict()
        
        for item in results['tracks']['items']:
            track_name = item['name']
            artist_name = item['artists'][0]['name']
            tracks[track_name] = artist_name
        
        return tracks