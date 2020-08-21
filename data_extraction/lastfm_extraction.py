import requests
import time
import pandas
import csv
'''
    1. Get top tags by popularity
    2. For each tag, get top artists
    3. For each artist, get top tracks
'''

class LastFmExtractor:

    def __init__(self, API_KEY):
        self.BASE_URL = 'http://ws.audioscrobbler.com'
        self.TAGS_URL = '/2.0/?method=tag.getTopTags&api_key=' + API_KEY + '&format=json'
        self.ARTISTS_URL = '/2.0/?method=tag.gettopartists&api_key=' + API_KEY + '&format=json&limit=300'
        self.TRACKS_URL = '/2.0/?method=artist.gettoptracks&api_key=' + API_KEY + '&format=json&limit=300'

    def _callAPI(self, url):
        response = requests.get(self.BASE_URL + url)
        return response.json()

    '''
        out: [{'name':tag,
               'count': number of times used,
               'reach': undefined
              },...]
    '''
    def _getTopTags(self):
        tags_json = self._callAPI(self.TAGS_URL)
        return tags_json['toptags']['tag']

    '''
        out: [{'tag': [{'name':,'mbid':,'url':...},..]},...]
    '''
    def _getTopArtists(self, tags):
        tag_artists = {}
        for tag_dict in tags:
            tag = tag_dict['name']
            thisUrl = self.ARTISTS_URL + '&tag=' + tag
            artists_json = self._callAPI(thisUrl)
            tag_artists[tag] = artists_json['topartists']['artist']
            time.sleep(1)
        return tag_artists


    def _getTopTracks(self, artists):
        all_tracks = []
        for tag, artists in artists.items():
            for artist in artists:
                thisArtist = artist['name'].replace(" ", '+')
                thisUrl = self.TRACKS_URL + '&artist=' + thisArtist
                response = self._callAPI(thisUrl)
                print(response)
                if 'toptracks' not in response.keys():
                    continue
                tracks = response['toptracks']['track']
                for i in range(len(tracks)):
                    tracks[i]['tag_name'] = tag
                all_tracks.append(tracks)

                time.sleep(0.10)
        return all_tracks

    def extractData(self):
        print("Retrieving tags...")
        tags = self._getTopTags()

        print("Tags retrieved. Retrieving corresponding artists...")
        artists = self._getTopArtists(tags)

        print("Artists retrieved. Retrieving corresponding tracks...")
        trackList = self._getTopTracks(artists)


        print("Writing to CSV...")
        f = csv.writer(open("tracks_increased_limit_300.csv", 'w'))

        f.writerow(['name', 'tag_name', 'playcount', 'listeners', 'artist_name'])

        for tracks in trackList:
            for x in tracks:
                f.writerow([x["name"],
                            x["tag_name"],
                            x["playcount"],
                            x["listeners"],
                            x["artist"]["name"]])

        print("Extraction completed!")


if __name__ == '__main__':
    API_KEY = 'fc8be3717cce656fc0cc56a96707d51e'

    extractor = LastFmExtractor(API_KEY)

    print("Started extraction!")
    extractor.extractData()

