import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pytube import YouTube
from youtube_search import YoutubeSearch
from moviepy.editor import VideoFileClip
from moviepy.editor import AudioFileClip
def get_playlist_tracks(playlist_id):
    # Initialize Spotipy client
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='acec26f255f34fa5aac641be2543defa',
                                                   client_secret='303c462a132d44f0b14aa053d513fee0',
                                                   redirect_uri='http://example.com',
                                                   scope='playlist-modify-public'))

    # Retrieve playlist tracks
    playlist_tracks = sp.playlist_tracks(playlist_id)
    tracks = []
    for item in playlist_tracks['items']:
        track = item['track']
        tracks.append(track['name'])
    return tracks

    # Search for videos related to the query
def search_and_download(query):
        # Search for videos related to the query
        results = YoutubeSearch(query, max_results=1).to_dict()

        if not results:
            print(f"No videos found for the query: {query}")
            return

        video_id = results[0]['id']
        video_title = results[0]['title']

        youtube_url = f"https://www.youtube.com/watch?v={video_id}"
        try:
            yt = YouTube(youtube_url)
            video = yt.streams.filter(only_audio=True).first()
            # Save the audio file with the name of the song
            audio_file = video.download(filename=video_title)
        except Exception as e:
            print(f"An error occurred while downloading the video for the song '{query}':", e)
            return

        # Create a folder named "my_songs" if it doesn't exist
        folder_name = "my_songs"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        # Set the path for the MP3 file inside the "my_songs" folder
        mp3_file = os.path.join(folder_name, os.path.splitext(os.path.basename(audio_file))[0] + ".mp3")

        try:
            video_clip = AudioFileClip(audio_file)
            video_clip.write_audiofile(mp3_file)
            video_clip.close()
        except Exception as e:
            print("An error occurred while converting the video to MP3:", e)
            return

        # Delete the original video file
        os.remove(audio_file)

        print(f"Downloaded MP3: {mp3_file}")
        return mp3_file


# Specify the playlist ID
playlist_id = 'https://open.spotify.com/playlist/7bJVlIrnaYBQkP3Y5gAOUc?si=cac55d30f07b4ebe'

# Retrieve tracks from the playlist
tracks = get_playlist_tracks(playlist_id)

# Print the names of the tracks
print("Songs in the playlist:")
for track in tracks:
    print(track)
    search_and_download(track)







