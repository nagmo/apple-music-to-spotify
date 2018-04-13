import pprint
import spotipy
import spotipy.util as util
import untangle

#user data
file = './Library.xml'
SPOTIPY_CLIENT_ID='0a9ac178f4544d1393f95f5bc78bf6b8'
SPOTIPY_CLIENT_SECRET='386ab1e4d8934af19d64677742ba3fac'
SPOTIPY_REDIRECT_URI='http://google.co.il/'
username = 'nagmo92'

def in_apple_music(track):
    for key in track.key:
        if key.cdata == 'Apple Music':
            return True
    return False


def get_data(track, data):
    for i in range(len(track.key)):
        if track.key[i].cdata == data:
            return track.string[i-1].cdata


lib = untangle.parse(file)
xmlTracks = [xmlTrack for xmlTrack in lib.plist.dict.dict.dict if in_apple_music(xmlTrack)]
tracks = []
for xmlTrack in xmlTracks:
    tracks.append({'Name': get_data(xmlTrack, 'Name'),
                   'Artist': get_data(xmlTrack, 'Artist'),
                   'Album': get_data(xmlTrack, 'Album')})

scope = 'user-library-modify'
token = util.prompt_for_user_token(username,scope,client_id=SPOTIPY_CLIENT_ID,client_secret=SPOTIPY_CLIENT_SECRET,redirect_uri=SPOTIPY_REDIRECT_URI)

if token:
    sp = spotipy.Spotify(auth=token)

    trackURIs = []
    notFound = []

    for track in tracks[:100]:
        results = sp.search(q=track['Name'], limit=20)
        if not results['tracks']['items']:
            notFound.append(track)
        else:
            trackURI = results['tracks']['items'][0]['uri']
            trackURIs.append(trackURI)

    pprint.pprint(trackURIs)
    #results = sp.current_user_saved_tracks_add(tracks=trackURIs)
    #pprint.pprint(results)
    pprint.pprint(notFound)

else:
    print("Can't get token for", username)