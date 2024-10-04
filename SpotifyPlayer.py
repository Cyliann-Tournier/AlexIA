import spotipy
from spotipy.oauth2 import SpotifyOAuth

class SpotifyPlayer:
    
    def __init__(self, client, secret, uri, scope) -> None:
        self.client = client
        self.secret = secret
        self.uri = uri
        self.scope = scope
        self.sp_oauth = SpotifyOAuth(client_id=self.client, 
                                      client_secret=self.secret, 
                                      redirect_uri=self.uri,
                                      scope=self.scope)
        self.spotify = spotipy.Spotify(auth_manager=self.sp_oauth)

    def get_devices(self):
        devices = self.spotify.devices()
        return devices['devices']

    def playSong(self, track_uri):
        device_name = "CT"
        self.devices = self.get_devices() 
        print(f"Appareils disponibles : {[device['name'] for device in self.devices]}")  # Affiche les appareils disponibles

        device_id = None
        for device in self.devices:
            if device['name'].lower() == device_name.lower():
                device_id = device['id']
                break

        if device_id:
            print(f"Lecture sur l'appareil : {device_name}")

            try:
                self.spotify.start_playback(device_id=device_id, uris=[track_uri])
                print("Lecture en cours...")
            except spotipy.exceptions.SpotifyException as e:
                print(f"Erreur lors de la lecture : {e}")
        else:
            print(f"Aucun appareil trouvé avec le nom : {device_name}")
        
        return "Dis que tu lances la lecture de la chanson qui t'a été demandée."

    def search_track(self, track_name):
        result = self.spotify.search(q=track_name, type='track', limit=1)

        if result['tracks']['items']:
            track = result['tracks']['items'][0]
            track_name = track['name']
            track_uri = track['uri']
            track_artist = track['artists'][0]['name']
            print(f"Track trouvé : {track_name} par {track_artist}")
            return track_uri
        else:
            print("Aucune piste trouvée pour ce nom.")
            return None
