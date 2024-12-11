#import playlist_maker
import flask_app
#from user_data import UserData

def main():
    """playlist_name, result = app.get_playlist_information()
    song_dictionary = app.create_song_dictionary(result)
    user_id = app.get_user_id()
    app.create_playlist(playlist_name, user_id,song_dictionary)"""
    flask_app.app.run(host = "0.0.0.0", port =8000, debug = True)
    #playlist_maker.get_user_id()
if __name__ == "__main__":
    main()