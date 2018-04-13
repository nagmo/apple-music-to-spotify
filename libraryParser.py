import untangle


def in_apple_music(track):
    for key in track.key:
        if key.cdata == 'Apple Music':
            return True
    return False


def get_data(track, data):
    for i in range(len(track.key)):
        if track.key[i].cdata == data:
            return track.string[i-1].cdata

file = './Library.xml'
lib = untangle.parse(file)
xmlTracks = [xmlTrack for xmlTrack in lib.plist.dict.dict.dict if in_apple_music(xmlTrack)]
tracks = []
for xmlTrack in xmlTracks:
    tracks.append({'Name': get_data(xmlTrack, 'Name'),
                   'Artist': get_data(xmlTrack, 'Artist'),
                   'Album': get_data(xmlTrack, 'Album')})
    
print(tracks[:10])
