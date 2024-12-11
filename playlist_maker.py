from langchain.llms import OpenAI
from langchain.agents import initialize_agent, Tool
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_core.messages import HumanMessage
import Prompts
import models
import ast
from collections import defaultdict

"""TO-DO: make this a class so that i can modularise the code"""

class GeneratedPlaylist:

    def __init__(self,user_id,personal_data):
        self.user_id = user_id
        self.personal_data = personal_data

    # this is the only function that needs to be called anywhere else
    def generate_playlist(self,data: dict,top_recommendations: defaultdict) -> tuple:
        playlist_name = data["playlist_name"]
        num_songs = data["num_songs"]
        user_input = data["user_prompt"]

        result = self.generate_songs(num_songs, user_input,top_recommendations)
        song_dictionary = self.create_song_dictionary(result)
        print(f'The songs suggested by LLM are {song_dictionary}')
        self.create_playlist_in_spotify(playlist_name,song_dictionary)

        return playlist_name, num_songs, user_input
    
    #this generates songs from the llm 
    def generate_songs(self, num_songs, user_input, top_songs:defaultdict):
        AI_Playlist = PromptTemplate(
            input_variables=["personal_data","user_input","num_songs","top_songs"],
            template= Prompts.GeneratePlaylist_SYSTEM_PROMPT)

        formatted_prompt = AI_Playlist.format(
            personal_data= self.personal_data,
            user_input= user_input,
            num_songs = num_songs,
            top_songs = top_songs
        )
        response = models.llm.invoke([HumanMessage(content=formatted_prompt)])
        result = response.content.strip()
        return result

    #this converts result to a dictionary
    def create_song_dictionary(self,result):
        song_dictionary = ast.literal_eval(result)
        return song_dictionary

    #this gets the urls of the songs
    def get_song_urls(self,songname: str, artist_name: str = None):
        results = models.sp.search(q='track:' + songname, type='track')
        items = results['tracks']['items']
        if len(items) > 0:
            track_results = items[0:20]  
            for track in track_results:
                track_artist = track['artists'][0]['name']
                
                if artist_name is None or artist_name.lower() in track_artist.lower():
                        #print(f'tracks are {track['uri']}')
                        return track['uri']

    #this creates a playlist in the user_account
    def create_playlist_in_spotify(self,playlist_name,song_dictionary):
        playlist_name = playlist_name
        playlist_description = "This is a playlist I created with Spotipy and Python"
        new_playlist = models.sp.user_playlist_create(user=self.user_id, name=playlist_name, public=True, description=playlist_description)

        track_uris = list()
        for key,value in song_dictionary.items():
            track = self.get_song_urls(key,value)
            if track:
                track_uris.append(track)
        if track_uris:
            models.sp.playlist_add_items(new_playlist['id'], track_uris)
            
    """def get_playlist_information(self):
        print("Hi! Let's create the perfect playlist for you. First, some basic questions: \n")
        playlist_name = input("What would you like your playlist to be called? \n")
        num_songs = input("How many songs would you like in your playlist? \n")
        print("Now, give me some more detailed information....\n")
        user_input = input("What kind of playlist would you like?\n")
        result = self.generate_playlist(num_songs,user_input)
        return (playlist_name, result)"""