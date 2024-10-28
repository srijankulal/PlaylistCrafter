# import pandas as pd
import os
from flask import Flask, session, redirect, url_for , request ,render_template ,jsonify, flash
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler
from dotenv import load_dotenv
import random as rd

load_dotenv()
app=Flask(__name__,template_folder='Templates')

app.config["SECRET_KEY"]=os.getenv("Secret_key")

client_id=os.getenv("Client_ID")
client_secret=os.getenv("Client_SECRET")
redirect_url1="http://127.0.0.1:5000/callback"
redirect_url2="http://qc1hlnwn-5000.inc1.devtunnels.ms//callback"
redirect_url="https://playlistcrafter.vercel.app/callback"
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




@app.route('/')
#main page 
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')

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
    playlistName1= request.form['playlist_name1']
    playlist_id2 = request.form['playlistId2']
    playlistName2= request.form['playlist_name2']
    if playlist_id1 and playlist_id2:
        if playlist_id1!= playlist_id2:
            songsFromPlaylist1=get_all_playlist_tracks(playlist_id1)#results are the id of the songs
            songsFromPlaylist2=get_all_playlist_tracks(playlist_id2)
            FinalPlaylistIds=createBlend(songsFromPlaylist1,songsFromPlaylist2)
            user_id = sp.current_user()['id']
            playlist = sp.user_playlist_create(user_id, f"Blended Playlist", public=True,collaborative=False,description=f"{playlistName1} + {playlistName2}")
            playlist_id = playlist['id']
    
    # Add tracks to the playlist in chunks easy no stress 
            for chunk in chunk_list(FinalPlaylistIds, 100):
                sp.playlist_add_items(playlist_id, chunk)
            # print(playlist)
            playlist_url=playlist['external_urls']['spotify']
            # print(playlist_url)
            return jsonify({"playlist_url": playlist_url})


    

def get_all_playlist_tracks(playlist_id):#this function is used to get all the songs id from the playlist and send only ids
    all_tracks = []
    results = sp.playlist_tracks(playlist_id)
    all_tracks.extend(results['items'])

    while results['next']:#nexr because default limit is 100 so if there are more than 100 songs then we have to use next
        results = sp.next(results)
        all_tracks.extend(results['items'])
    #returns just id of all the songs 
    all_tracks = [track['track']['id'] for track in all_tracks]
    return all_tracks

def chunk_list(lst, chunk_size):
    """Helper function to split a list into chunks."""
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]

#This function is to create final list of songs 
def createBlend(songsFromPlaylist1 ,songsFromPlaylist2):
    list1=songsFromPlaylist1
    list2=songsFromPlaylist2
    
    blendLimit=(len(list1)+len(list2))//2
    finList=list1+list2
    rd.shuffle(finList)
    blendList=finList[:blendLimit]
    # Remove duplicate IDs
    seen = set()
    unique_blendList = []
    for song in blendList:
        if song not in seen:
            unique_blendList.append(song)
            seen.add(song)
    
    return unique_blendList



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
            results = sp.search(q=playlist_name, limit=10, type='playlist')
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
