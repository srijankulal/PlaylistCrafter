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
redirect_url="https://playlistcrafter.vercel.app/callback"
scope = 'user-read-recently-played user-top-read user-library-read playlist-read-private playlist-modify-public playlist-modify-private user-read-private user-read-email'

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

@app.route('/')
#simple html for user to promot 
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
    return render_template('./SongSync/songSync.html')

@app.route('/moodSync')
def mood():
    return render_template('./MoodSync/mood.html')

@app.route('/auth_similarLogin')
def similarLogin():
    session['auth_route'] = 'similarLogin'
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):# to check if user logined or not 
        auth_url = sp_oauth.get_authorize_url()
        
        return redirect(auth_url)
        # return f'<a href="{auth_url}">Login to Spotify</a>'
    return redirect(url_for('similar'))
    

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
        return redirect("/songSync")

    code = request.args.get('code')
    if not code:
        return  redirect(url_for("home"))

    sp_oauth.get_access_token(code)
    session['logged_in'] = True
    if session.get('auth_route') == 'similarLogin':
        return redirect(url_for("similar"))
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
    session['auth_route'] = 'similarLogin'
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)

    # user_profile = sp.current_user()
    # profile_picture_url = user_profile.get('images', [{}])[0].get('url', None)
    # session['profile_pic_url'] = profile_picture_url
    # print(session['profile_pic_url'])
    

    return redirect(url_for('similar'))

@app.route('/profile_pic')
def get_pic():
    user_profile = sp.current_user()
    profile_picture_url = user_profile.get('images', [{}])[0].get('url', None)
    
    # Return the profile picture URL as JSON
    return jsonify({'profile_picture_url': profile_picture_url})
    
    
    

@app.route('/logout')
def logout():
    session.clear() #clear the session
    session.pop('logged_in', None)
    return redirect(url_for('similar'))


if __name__=="__main__":
    app.run(debug=True)
