from ytmusicapi import YTMusic
import sys
import spotipy
from spotipy.oauth2 import SpotifyOAuth

arguments = sys.argv[1:]

source_playlist_id = arguments[0]
destination_playlist_name = arguments[1]

# Spotify Data Scraping

spotify_client_id = '0d387bee1a1a414ca42f9bcbde50dc81'
spotify_client_secret = 'c7aa5ae0b2d24df286e4eaae7afb40c3'
redirect_uri = 'http://localhost:3000/callback'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="user-library-read",
                     client_id=spotify_client_id, client_secret=spotify_client_secret, redirect_uri=redirect_uri, cache_path=".cache_sp.json"))

per_page = 100
current_page = 0
max_pages = 0

song_queries = []

print('Gathering all songs from Spotify playlist', source_playlist_id, '...')

while True:
    items = sp.playlist_items(
        source_playlist_id, limit=per_page, offset=current_page * per_page)['items']

    for item in items:
        if item['is_local']:
            continue
        song = item['track']['name']
        author = item['track']['artists'][0]['name']
        song_queries.append(str(author + " " + song))

    current_page = current_page + 1

    if len(items) != per_page or (max_pages != 0 and current_page >= max_pages):
        break

print("Gathered", len(song_queries),
      "songs from Spotify to be migrated. Now searching on Youtube Music...")

# Youtube Delivery

yt = YTMusic('.cache_yt.json')

songs = []
for i, query in enumerate(song_queries):
    query_results = yt.search(query, filter="songs")
    if len(query_results) == 0:
        continue
    song = query_results[0]
    print("Found " + str(i + 1) + ':',
          str(song['artists'][0]['name'] + " - " + song['title']))
    songs.append(song['videoId'])

if len(songs) > 0:
    print("Creating playlist", destination_playlist_name, '...')
    playlist_id = yt.create_playlist(
        destination_playlist_name, "this is an auto-generated playlist")
    print("Adding", len(songs), 'songs to playlist ...')
    response = yt.add_playlist_items(playlist_id, songs, duplicates=True)
    print("All songs added. Enjoy your brand new Youtube Music playlist!")
