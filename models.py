from langchain.chat_models import ChatOpenAI
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
from facebook_bart import FacebookBART

load_dotenv()

#openai stuff
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

llm = ChatOpenAI(
    api_key = OPENAI_API_KEY
)

#spotipy stuff
SPOTIPY_CLIENT_ID = os.environ["SPOTIPY_CLIENT_ID"]
SPOTIPY_CLIENT_SECRET = os.environ["SPOTIPY_CLIENT_SECRET"]
SPOTIPY_REDIRECT_URI = os.environ["SPOTIPY_REDIRECT_URI"]
SPOTIPY_SCOPE = os.environ["SPOTIPY_SCOPE"]

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope=SPOTIPY_SCOPE))

#bart stuff
HUGGING_FACE_TOKEN = os.environ['HUGGING_FACE_TOKEN']
BART_API_URL = os.environ['BART_API_URL']

bart = FacebookBART(token=HUGGING_FACE_TOKEN, url=BART_API_URL)