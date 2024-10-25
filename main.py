# import pandas as pd
import os
from flask import Flask, session, redirect, url_for , request ,render_template ,jsonify, flash
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler
from dotenv import load_dotenv

load_dotenv()
app=Flask(__name__,template_folder='Templates')

app.config["SECRET_KEY"]=os.getenv("Secret_key")

client_id=os.getenv("Client_ID")
client_secret=os.getenv("Client_SECRET")
redirect_url="http://127.0.0.1:5000/callback"
scope = 'user-read-recently-played user-top-read user-library-read playlist-read-private playlist-modify-public playlist-modify-private user-read-private user-read-email playlist-read-collaborative'

cache_handler = FlaskSessionCacheHandler(session)#to store the token in flask
sp_oauth=SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_url,
    scope=scope,
    cache_handler=cache_handler,
    show_dialog=False #debugg    git commit -m "Initial commit"
)
sp = Spotify(auth_manager=sp_oauth)

# Mood ranges dictionary
# mood_ranges = {
#     'angry': {'valence': (0.0, 0.3), 'energy': (0.7, 1.0)},
#     'frustrated': {'valence': (0.2, 0.4), 'energy': (0.6, 0.8)},
#     'irritated': {'valence': (0.2, 0.4), 'energy': (0.5, 0.7)},
#     'annoyed': {'valence': (0.3, 0.5), 'energy': (0.5, 0.7)},
#     'upset': {'valence': (0.1, 0.3), 'energy': (0.4, 0.6)},
#     'disgusted': {'valence': (0.0, 0.2), 'energy': (0.4, 0.6)},
#     'sad': {'valence': (0.0, 0.3), 'energy': (0.0, 0.5)},
#     'miserable': {'valence': (0.0, 0.2), 'energy': (0.1, 0.4)},
#     'gloomy': {'valence': (0.1, 0.3), 'energy': (0.2, 0.4)},
#     'dejected': {'valence': (0.0, 0.2), 'energy': (0.1, 0.3)},
#     'bored': {'valence': (0.2, 0.4), 'energy': (0.2, 0.4)},
#     'tired': {'valence': (0.1, 0.3), 'energy': (0.1, 0.3)},
#     'relaxed': {'valence': (0.5, 0.7), 'energy': (0.2, 0.4)},
#     'calm': {'valence': (0.5, 0.7), 'energy': (0.1, 0.3)},
#     'serene': {'valence': (0.6, 0.8), 'energy': (0.2, 0.4)},
#     'happy': {'valence': (0.7, 1.0), 'energy': (0.6, 1.0)},
#     'contented': {'valence': (0.7, 0.9), 'energy': (0.4, 0.6)},
#     'pleased': {'valence': (0.7, 0.9), 'energy': (0.5, 0.7)},
#     'joy': {'valence': (0.8, 1.0), 'energy': (0.7, 1.0)},
#     'ecstatic': {'valence': (0.9, 1.0), 'energy': (0.8, 1.0)},
#     'excited': {'valence': (0.8, 1.0), 'energy': (0.8, 1.0)},
#     'surprised': {'valence': (0.7, 0.9), 'energy': (0.7, 0.9)},
#     'astonished': {'valence': (0.8, 1.0), 'energy': (0.7, 0.9)},
#     'amused': {'valence': (0.6, 0.8), 'energy': (0.5, 0.7)},
#     'engaged': {'valence': (0.6, 0.8), 'energy': (0.6, 0.8)},
#     'alarmed': {'valence': (0.3, 0.5), 'energy': (0.7, 0.9)},
#     'shocked': {'valence': (0.2, 0.4), 'energy': (0.7, 0.9)},
#     'neutral': {'valence': (0.4, 0.6), 'energy': (0.4, 0.6)},
#     'apathetic': {'valence': (0.3, 0.5), 'energy': (0.3, 0.5)},
#     'concerned': {'valence': (0.4, 0.6), 'energy': (0.5, 0.7)},
#     'contemplative': {'valence': (0.4, 0.6), 'energy': (0.3, 0.5)},
#     'relief': {'valence': (0.5, 0.7), 'energy': (0.3, 0.5)},
#     'at ease': {'valence': (0.5, 0.7), 'energy': (0.2, 0.4)},
#     'drowsy': {'valence': (0.3, 0.5), 'energy': (0.1, 0.3)},
#     'sleepy': {'valence': (0.2, 0.4), 'energy': (0.1, 0.2)}
# }

# def get_track_features(track_id):
#     features = sp.audio_features([track_id])[0]
#     return {
#         'danceability': features['danceability'],
#         'energy': features['energy'],
#         'valence': features['valence']
#     }

# def recommend_by_mood(mood):
#     selected_range = mood_ranges.get(mood)
#     if not selected_range:
#         return []

#     results = sp.search(q='.', type='track', limit=50)

#     recommendations = []
#     for track in results['tracks']['items']:
#         features = get_track_features(track['id'])
#         if (selected_range['valence'][0] <= features['valence'] <= selected_range['valence'][1] and
#             selected_range['energy'][0] <= features['energy'] <= selected_range['energy'][1]):
#             recommendations.append(track['name'])

#     return recommendations






@app.route('/')
#main page 
def home():
    return render_template('home.html')



@app.route('/auth')
def auth():
    session['auth_route'] = 'home'
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):# to check if user logined or not 
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
        # return f'<a href="{auth_url}">Login to Spotify</a>'
    return redirect(url_for('home'))

@app.route('/songSync')
def similar():
    session['auth_route']='similarLogin'
    return render_template('./SongSync/songSync.html')

# @app.route('/moodSync')
# def mood():
#     return render_template('./MoodSync/mood.html')


# @app.route('/recommend', methods=['POST'])
# def recommend():
#     mood = request.form['mood']
#     recommendations = recommend_by_mood(mood)
#     return render_template('./MoodSync/recommend.html', mood=mood, recommendations=recommendations)

@app.route('/playlistBlend')
def blends():
    session['auth_route']='blendLogin'
    return render_template('./PlaylistBlend/playlistBlend.html')#, playlists=playlists['items'],playlists2=playlists2['items']




@app.route('/auth_similarLogin')#check spotify login and logout details in similar page
def similarLogin():
    session['auth_route'] = 'similarLogin'
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):# to check if user logined or not 
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
        # return f'<a href="{auth_url}">Login to Spotify</a>'
    return redirect(url_for('similar'))#here similar is function name for songsync page
    
@app.route('/auth_blendLogin')#check spotify login and logout details in blend page
def blendLogin():
    session['auth_route'] = 'blendLogin'
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    return redirect(url_for('blends'))#here blends is function name for playlistblend page

@app.route('/blend_playlists', methods=['POST'])#blends the playlist and create a new playlist with the songs of both playlist
def blend_playlists():
    playlist_id1 = request.form['playlistId1']
    playlist_id2 = request.form['playlistId2']
    if playlist_id1 and playlist_id2:
        songsFromPlaylist1=get_all_playlist_tracks(playlist_id1)#results are the id of the songs
        songsFromPlaylist2=get_all_playlist_tracks(playlist_id2)
        # print(playlist_id1)
        # print(playlist_id2)
        # for list in songsFromPlaylist1:
        #     print(list['track']['name'])
        # for list2 in songsFromPlaylist1:
        #     print(list2['track']['name'])
        # # store the songs in a text file 
        # with open('songsFromPlaylist1.txt', 'w') as f:
        #     for song in songsFromPlaylist1:
        #         f.write(f"{song['track']['name']} - {song['track']['artists'][0]['name']}\n")
        # with open('songsFromPlaylist2.txt', 'w') as f:
        #     for song in songsFromPlaylist2:
        #         f.write(f"{song['track']['name']} - {song['track']['artists'][0]['name']}\n")
        
        
        # songsFromPlaylist1 = sp.playlist_tracks(playlist_id1)['items']
        # songsFromPlaylist2 = sp.playlist_tracks(playlist_id2)['items']
        
        
    return
def get_all_playlist_tracks(playlist_id):
    all_tracks = []
    results = sp.playlist_tracks(playlist_id)
    all_tracks.extend(results['items'])

    while results['next']:
        results = sp.next(results)
        all_tracks.extend(results['items'])
    #return just id of all the songs only
    all_tracks = [track['track']['id'] for track in all_tracks]
    return all_tracks
    
@app.route('/create_playlist', methods=['POST'])
def create_playlist():
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):# to check if user logined or not 
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    song_name = request.form['song_name']
    song_id = request.form['song_id']
    if song_id:
        track=sp.track(song_id)
        recommendations = sp.recommendations(seed_tracks=[song_id], limit=20)['tracks']
        track_ids = [track['id'] for track in recommendations]
        user_id = sp.current_user()['id']
        playlist = sp.user_playlist_create(user_id,f"Playlist based on {song_name}",public=True)
        sp.playlist_add_items(playlist['id'],track_ids)
        playlist_url=playlist['external_urls']['spotify']
    
        return jsonify({"playlist_url": playlist_url})
    return jsonify({"playlist_url": None})

# @app.route('/create_mood',methods=['POST'])
# def mood_playlist():
    
    
    
    
    
    
    
@app.route('/autocomplete', methods=['GET'])# to get the song name suggestion
def autocomplete():
    song_name = request.args.get('song_name', '')
    suggestions = []
    if song_name:
            results = sp.search(q=song_name, limit=8, type='track')
            tracks = results['tracks']['items'] #to store the output in a list 
            suggestions = [{
                'id': track['id'],
                'name': track['name'],
                'artist': track['artists'][0]['name'],
                'cover_image': track['album']['images'][0]['url'] if track['album']['images'] else None
            } for track in tracks]
    return jsonify(suggestions)

@app.route('/autocompletePlaylist', methods=['GET'])# to get the playlist name suggestion
def autocompletePlaylist():
    playlist_name = request.args.get('playlist_name', '')
    suggestions = []
    if playlist_name:
            results = sp.search(q=playlist_name, limit=6, type='playlist')
            playlists = results['playlists']['items']
            suggestions = [{
                'id': playlist['id'],
                'name': playlist['name'],
                'owner': playlist['owner']['display_name'] if 'owner' in playlist else 'Unknown',
                'cover_image': playlist['images'][0]['url'] if playlist['images'] else None
            } for playlist in playlists]
    return jsonify(suggestions)

@app.route('/callback')
def callback():
    error = request.args.get('error')
    if error:
        session.pop('logged_in', None)
        if error == 'access_denied':
            flash("Access denied by user. Please try again.", "error")
        else:
            flash(f"Authorization failed: {error}", "error")
            referrer = request.referrer
            if referrer.endswith('/songSync'):
                return redirect("/songSync")
            elif referrer.endswith('/playlistBlend'):
                return redirect("/playlistBlend")
        return redirect(url_for("home"))
        # return redirect("/songSync")
    code = request.args.get('code')
    referrer = request.referrer
    if not code:
        return  redirect(url_for("home"))
    sp_oauth.get_access_token(code)
    session['logged_in'] = True
    if session['auth_route']=='similarLogin':
        return redirect("/songSync")
    elif session['auth_route']=='blendLogin':
        return redirect("/playlistBlend")
    else:
        return redirect(url_for("home"))

# @app.route('/get_playlist')
# def get_playlist():
#     if not sp_oauth.validate_token(cache_handler.get_cached_token()):# to check if user logined or not 
#         auth_url = sp_oauth.get_authorize_url()
#         return redirect(auth_url)

#     playlist=sp.current_user_playlists()
#     playlist_info=[(pl['name'],pl['external_urls']['spotify']) for pl in playlist['items']]
#     playlist_html = '<br>'.join([f'{name}: {url}' for name, url in playlist_info])
    
#     return playlist_html

@app.route('/login')
def login():
    
    referrer = request.referrer#check the function call request from which page
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    if session['auth_route']=='similarLogin':
        return redirect("/songSync")
    elif session['auth_route']=='blendLogin':
        return redirect("/playlistBlend")
    else:
        return redirect(url_for("home"))

@app.route('/profile_pic')
def get_pic():
    user_profile = sp.current_user()
    try:#try block because if no profile pic then there is an exception by spotify
        profile_picture_url = user_profile.get('images', [{}])[0].get('url', None)
        return jsonify({'profile_picture_url': profile_picture_url})# Return the profile picture URL as JSON
    except:#using except block i can return none if there is no profile pic
        return jsonify({'profile_picture_url': "None"})
    
        
    
    
    

@app.route('/logout')
def logout():
    session.clear() #clear the session
    session.pop('logged_in', None)
    referrer = request.referrer
    if referrer.endswith('/songSync'):
        return redirect(url_for('similar'))
    elif referrer.endswith('/playlistBlend'):
        return redirect(url_for('blends'))
    return redirect(url_for('home'))


if __name__=="__main__":
    app.run(debug=True)
