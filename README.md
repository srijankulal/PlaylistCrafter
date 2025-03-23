# Playlist Crafter

PlaylistCrafter is a web application that leverages the Spotify API to help users discover new music and create customized playlists.

## Features

- **Song Sync**: Create playlists of songs similar to a track you love. Simply search for your favorite music, and the app will curate a collection of tracks with a similar vibe.
- **Playlist Blend**: Combine two different playlists to create a new unique playlist, perfect for mixing genres or discovering the intersection of musical tastes.
- **Spotify Integration**: Seamlessly connect with your Spotify account to access and manage your playlists directly from the app.

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **APIs**: Spotify Web API
- **Authentication**: OAuth 2.0 via Spotify OAuth
- **Deployment**: Vercel

## Setup and Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/PlaylistCrafter.git
   cd PlaylistCrafter
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a .env file in the root directory with the following variables:
   ```
   Client_ID=your_spotify_client_id
   Client_SECRET=your_spotify_client_secret
   Secret_key=your_flask_secret_key
   ```

4. Run the application:
   ```bash
   python main.py
   ```

5. Visit `http://127.0.0.1:5000` in your browser to use the application locally.

## How to Use

### Song Sync
1. Navigate to the Song Sync page
2. Connect your Spotify account
3. Search for a song you like
4. Select it from the search results
5. Click "Create Playlist" to generate a playlist of similar songs

### Playlist Blend
1. Navigate to the Playlist Blend page
2. Connect your Spotify account
3. Search for and select two playlists
4. Click "Blend Playlists" to create a new playlist combining songs from both

## Project Structure

```
PlaylistCrafter/
├── main.py                  # Main Flask application
├── requirements.txt         # Python dependencies
├── vercel.json              # Vercel deployment configuration
├── static/                  # Static files
│   ├── css/                 # CSS stylesheets
│   └── Images/              # Images and icons
└── Templates/               # HTML templates
    ├── home.html
    ├── about.html
    ├── PlaylistBlend/
    │   └── playlistBlend.html
    └── SongSync/
        └── songSync.html
```

## Future Enhancements

- Mood-based playlist generation
- Integration with other music platforms
- Enhanced filtering and customization options
- User profile and playlist history

## Contribution

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [Spotify Web API](https://developer.spotify.com/documentation/web-api)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Spotipy Library](https://spotipy.readthedocs.io/)
- Background CSS animation by [Ksenia Kondrashova](https://codepen.io/ksenia-k)
- Loading animation by [Vineeth.TR](https://github.com/vineethtrv)

## Contact

- [GitHub](https://github.com/srijankulal)
- [LinkedIn](https://www.linkedin.com/in/srijan-kulal)
- Email: srijankulal1010@gmail.com
