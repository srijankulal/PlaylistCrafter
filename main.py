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
    # playlists = sp.current_user_playlists()
    # playlists2 = sp.current_user_playlists(offset=100)
    session['auth_route']='blendLogin'
    return render_template('./PlaylistBlend/playlistBlend.html')#, playlists=playlists['items'],playlists2=playlists2['items']


@app.route('/blend_playlists', methods=['POST'])
def blend_playlists():
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)

    # Get the playlist IDs from the form
    playlist1_id = request.form.get('playlist1_id')
    playlist2_id = request.form.get('playlist2_id')
    
    # Fetch tracks from both playlists
    playlist1_tracks = sp.playlist_tracks(playlist_id=playlist1_id, fields='items.track.id')
    playlist2_tracks = sp.playlist_tracks(playlist_id=playlist2_id, fields='items.track.id')

    # Combine tracks from both playlists (blending logic can be more complex)
    combined_tracks = [item['track']['id'] for item in playlist1_tracks['items']] + [item['track']['id'] for item in playlist2_tracks['items']]
    
    # Create a new blended playlist
    user_id = sp.current_user()['id']
    new_playlist = sp.user_playlist_create(user_id, "Blended Playlist", public=True)
    
    # Add tracks to the new playlist
    sp.playlist_add_items(new_playlist['id'], combined_tracks[:100])  # Spotify has a limit on how many tracks you can add at once
    
    return jsonify({"playlist_url": new_playlist['external_urls']['spotify']})

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



@app.route('/create_playlist', methods=['POST'])
def create_playlist():
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):# to check if user logined or not 
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    song_name = request.form['song_name']
    results = sp.search(q=song_name, limit=1, type='track')#gets the id
    tracks = results['tracks']['items']
    if not tracks:
        return "Song not found",404
    song_id = tracks[0]['id']
    recommendations = sp.recommendations(seed_tracks=[song_id], limit=20)['tracks']
    track_ids = [track['id'] for track in recommendations]
    user_id = sp.current_user()['id']
    playlist = sp.user_playlist_create(user_id,f"Playlist based on {song_name}",public=True)
    sp.playlist_add_items(playlist['id'],track_ids)
    playlist_url=playlist['external_urls']['spotify']
    
    return jsonify({"playlist_url": playlist_url})
    # return redirect(playlist['external_urls']['spotify'])

# @app.route('/create_mood',methods=['POST'])
# def mood_playlist():
    
    
    
    
    
    
    
@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    song_name = request.args.get('song_name', '')
    suggestions = []
    if song_name:
            results = sp.search(q=song_name, limit=8, type='track')
            tracks = results['tracks']['items']
            suggestions = [{
                'name': track['name'],
                'artist': track['artists'][0]['name'],
                'cover_image': track['album']['images'][0]['url'] if track['album']['images'] else None
            } for track in tracks]
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
