import firebase_admin
from firebase_admin import credentials,firestore

cred = credentials.Certificate("myspotipyapp-firebase-adminsdk-qwt7f-85fdce366c.json")
firebase_admin.initialize_app(cred)

spotipy_firebase_db = firestore.client()
