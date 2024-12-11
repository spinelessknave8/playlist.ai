from flask import Flask, request, jsonify, session
import playlist_maker 
import os
import authentication
import user_data
import models
import top_songs

app = Flask(__name__)
app.secret_key = os.urandom(24) #generate random secret key

@app.route('/login', methods=['POST'])
def login():
    user_id = authentication.log_user_in()
    session['user_id'] = user_id  #store the user id in the sessions

    return jsonify({"status": "success", "message": "User logged in", "user_id": user_id})


@app.route('/logout',methods=['POST'])
def logout():
    authentication.log_user_out()
    session.clear()
    return jsonify({"status":"success","message":"user logged out sucessfully"})


@app.route('/get_user_data',methods = ['GET'])
def get_user_data():
    cur_user_id = session.get('user_id')
    cur_user_data = user_data.UserData(user_id = cur_user_id)
    cur_user_data.save_user_info()
    data = cur_user_data.load_from_firebase()
    
    session['Current User Info'] = data
    
    print(f'data is {data}')

    return jsonify({"status":"success",
                    "message":f'User: {cur_user_id} data saved and loaded successfully',
                    "User Data":data})

@app.route('/generate_playlist', methods = ['POST']) #get song recommendations from the genres
def create_playlist():
    user_id = session.get('user_id')
    print(user_id)
    if not(session.get('user_id')):
        raise Exception("User is not authenticated. Please log in.")
    user_data = session.get('Current User Info')
    if not user_data:
        raise Exception("Please sync user data.")
    data = request.json #needs playlist_name, num_songs,user_prompt
    
    user_query = data['user_prompt']
    
    #get genres
    genres = models.bart.categorise(user_query)
    song_recommendations = top_songs.TopSongs(genre = genres)
    results = song_recommendations.get_all_top_songs()

    #put it all together to generate the playlist
    try:
        generated_playlist = playlist_maker.GeneratedPlaylist(user_id,user_data)
        playlist_name, num_songs, user_input = generated_playlist.generate_playlist(data = data, 
                                                                                    top_recommendations= results)
        response = {
            "status": "success",
            "message": f"Generated playlist '{playlist_name}' with {num_songs} songs",
            "user_input": user_input,
            "recommendations":results,
            "User Data": user_data #this is here for debugging purposes only
        }
        return jsonify(response)
    
    except KeyError as e:
        return jsonify({"status": "error", "message": f"Missing key: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": f"An error occurred: {str(e)}"}), 500
    

## delete after testing
