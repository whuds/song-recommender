import spotipy.oauth2
import spotipy
import spotipy.util
import sys
import pprint
import time
import json
import numpy as np
import csv
import os


# token = client.get_access_token()
class Spotify():
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

        client = spotipy.oauth2.SpotifyClientCredentials(client_id, client_secret)
        self.spot = spotipy.Spotify(client_credentials_manager=client)
        self.spot.trace=False
        self.count = 500


    def getTracks(self, csv_file_name):
        tracks = []
        with open(csv_file_name + '.csv', mode='r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')

            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                else:
                    tracks.append((row[0], row[1],row[2], row[3], row[4]))
                    line_count += 1
            print(f'Processed {line_count} lines.')
        return tracks


    def getTrackURIs(self, tracks, counter):
        time.sleep(1)
        URIs = []
        track_num = 0
        tracks_sampled = tracks[counter:counter+self.count]
        for track in tracks_sampled:
            track_num += 1
            if (track_num % 50 == 0):
                print('Getting URI for track : ' + str(track_num) + ' out of ' + str(len(tracks_sampled)))
            search = track[4] + ' ' + track[0]
            track_search_result = self.spot.search(search)
            if len(track_search_result['tracks']['items']) > 0:
                track_URI = track_search_result['tracks']['items'][0]['uri']
                URIs.append(track + (track_URI,))
        return URIs


    def getAudioFeatures(self, tracks_with_URIs):
        time.sleep(1)
        audio_features = []
        audio_feat_count = 0
        for i in range(len(tracks_with_URIs)):
            audio_feat_count += 1
            if (audio_feat_count % 50 == 0):
                print('Getting audio features for track : ' + str(audio_feat_count) + ' out of ' + str(len(tracks_with_URIs)))
            track_URI = tracks_with_URIs[i][5]
            features = self.spot.audio_features(track_URI)
            audio_features.append(tracks_with_URIs[i][0:5] + tuple(features))
        # audio features appended to each track tuple at end as dictionary
        return audio_features


    def saveToCSV(self, f, audio_features):
        for a in audio_features:
            if (a[0] != None and a[1] != None and a[2] != None and a[3] != None and a[4] != None and a[5] != None):
                f.writerow([a[0],
                            a[1],
                            a[2],
                            a[3],
                            a[4],
                            a[5]['danceability'],
                            a[5]['energy'],
                            a[5]['key'],
                            a[5]['loudness'],
                            a[5]['mode'],
                            a[5]['speechiness'],
                            a[5]['acousticness'],
                            a[5]['instrumentalness'],
                            a[5]['liveness'],
                            a[5]['valence'],
                            a[5]['tempo'],
                            a[5]['type'],
                            a[5]['id'],
                            a[5]['uri'],
                            a[5]['track_href'],
                            a[5]['analysis_url'],
                            a[5]['duration_ms'],
                            a[5]['time_signature']])


def main():
    counter = 1790000
    filename = 'spotify_audio_features'
    fullname = 'spotify_audio_features.csv'
    if os.path.exists(fullname):
        print('appending from existing output file')
        f = csv.writer(open(filename + '.csv', 'a'))
    else:
        print('creating new output file')
        f = csv.writer(open(filename + '.csv', 'w'))
        f.writerow(['name', 'tag_name', 'playcount', 'listeners', 'artist_name', 'rank', 'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'type', 'id', 'uri', 'track_href', 'analysis_url', 'duration_ms', 'time_signature'])
    client_id = '0e2b3b4176014b4d8343d556aa255c8a'
    client_secret = 'c090164440c54b9b9083414cabe03729'
    spotify = Spotify(client_id, client_secret)
    tracks_filename = 'lastfm_tracks'
    print('Getting tracks from ' + tracks_filename+ '.csv')
    tracks =  spotify.getTracks(tracks_filename)

    while counter < len(tracks):
        print('Getting unique track URIs from {0}th index'.format(counter))
        tracks_with_URIs = spotify.getTrackURIs(tracks, counter)

        print('Getting track audio features...')
        audio_features = spotify.getAudioFeatures(tracks_with_URIs)

        print('Saving track audio features to output')
        spotify.saveToCSV(f, audio_features)
        counter += 500


if __name__  == '__main__':
    main()

