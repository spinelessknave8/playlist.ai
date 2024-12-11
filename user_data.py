import models
from datetime import datetime, timedelta, timezone
from firebase_init import spotipy_firebase_db

class UserData:
    def __init__(self,user_id):
        self.user_id = user_id
        #remember to add feedback also which is a dict with timestamp:feedback
    
    #function to run everything
    def save_user_info(self):
        self.set_timestamp()
        self.set_top_tracks()
        self.set_top_artists()
        self.set_recently_played_tracks()
        self.set_saved_tracks()
        self.set_saved_albums()
        self.set_followed_artists()
        self.set_playlists()
        self.set_profile_info()
    
    #access and save to firebase
    def save_to_firebase(self,firebase_key,value_to_save):
        #check last_save if it exists or not
        doc = spotipy_firebase_db.collection('User Data').document(self.user_id).get()
        if doc.exists:
            last_save = doc.to_dict().get('last_save')
            last_save_datetime = datetime.strptime(last_save, "%B %d, %Y at %I:%M:%S %p UTC%z") if isinstance(last_save, str) else last_save
            if datetime.now(timezone.utc) - last_save_datetime < timedelta(weeks=1): #less than a week since last_save
                return
        data = {firebase_key:value_to_save}
        spotipy_firebase_db.collection('User Data').document(self.user_id).set(data, merge = True) #overwrite existing data if it exists for the user_id, else create a new object

    def load_from_firebase(self):
        data = spotipy_firebase_db.collection('User Data').document(self.user_id).get()
        if data.exists:
            data = data.to_dict()
            return data
    #relevant setter functions
    def set_top_tracks(self, limit=10, time_range='medium_term'): #choices are long_term, medium_term, short_term
        try:
            results = models.sp.current_user_top_tracks(limit=limit, time_range=time_range)
            top_tracks = [track['name'] for track in results['items']]
            self.save_to_firebase("top_tracks",top_tracks)
        except Exception as e:
            print(f"Error fetching top tracks: {e}")

    def set_top_artists(self, limit=10, time_range='medium_term'):
        try:
            results = models.sp.current_user_top_artists(limit=limit, time_range=time_range)
            top_artists = [artist['name'] for artist in results['items']]
            self.save_to_firebase("top_artists",top_artists)
        except Exception as e:
            print(f"Error fetching top artists: {e}")

    def set_recently_played_tracks(self, limit=10):
        try:
            results = models.sp.current_user_recently_played(limit=limit)
            recently_played_tracks = [item['track']['name'] for item in results['items']]
            self.save_to_firebase("recently_played_tracks",recently_played_tracks)
        except Exception as e:
            print(f"Error fetching recently played tracks: {e}")

    def set_saved_tracks(self, limit=10):
        try:
            results = models.sp.current_user_saved_tracks(limit=limit)
            saved_tracks = [track['track']['name'] for track in results['items']]
            self.save_to_firebase("saved_tracks",saved_tracks)
        except Exception as e:
            print(f"Error fetching saved tracks: {e}")

    def set_saved_albums(self, limit=10):
        try:
            results = models.sp.current_user_saved_albums(limit=limit)
            saved_albums = [album['album']['name'] for album in results['items']]
            self.save_to_firebase("saved_albums",saved_albums)
        except Exception as e:
            print(f"Error fetching saved albums: {e}")

    def set_followed_artists(self, limit=10):
        try:
            results = models.sp.current_user_followed_artists(limit=limit)
            followed_artists = [artist['name'] for artist in results['artists']['items']]
            self.save_to_firebase("followed_artists",followed_artists)
        except Exception as e:
            print(f"Error fetching followed artists: {e}")

    def set_playlists(self, limit=10):
        try:
            results = models.sp.current_user_playlists(limit=limit)
            playlists = [playlist['name'] for playlist in results['items']]
            self.save_to_firebase("playlists",playlists)
        except Exception as e:
            print(f"Error fetching playlists: {e}")
    
    def set_timestamp(self):
        self.save_to_firebase("last_save", datetime.now())

    def set_profile_info(self):
        try:
            profile = models.sp.current_user()
            profile_info = {
                'display_name': profile.get('display_name'),
                'email': profile.get('email'),
                'country': profile.get('country'),
                'product': profile.get('product')
            }
            self.save_to_firebase("profile_info",profile_info)
        except Exception as e:
            print(f"Error fetching profile information: {e}")
    
