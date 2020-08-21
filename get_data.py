# Convert HD5 files to CSV
# Extracts features from every song and save them as columns in our dataset
# Features extracted: artist_name, title, artist_location,
# release,hotttness, familiarity, danceability, duration,energy,
# loudness, year, tempo, analysis_rate, end_of_fade_in, key,
# key_confidence, mode, mode_confidence, start_of_fade_out,
# time_signature,time_signature_conf, track_id

import hdf5_getters
import os
import csv
import string
import pickle
import tables

# Debugging
#h5 = hdf5_getters.open_h5_file_read("/mnt/c/Users/Aumit/Desktop/final-proj/MillionSongSubset/data/A/A/A/TRAAADZ128F9348C2E.h5")
#title = hdf5_getters.get_artist_name(h5)
#h5.close()
#print title

#input path for data directory
data_dir = './data'
#input path for the song set pickle file
set_file = 'userSongs.p'
songSet = pickle.load(open(set_file,'rb'))

# Open the CSV file we will write to
with open("output_usersong_features.csv", 'wb') as csvfile:
    # Column headers
    # Currently only 4 features being extracted
    # We can add as many as we want, just seperate with commas
    csvfile.write("artist_name,title,artist_location,release,hotttness,familiarity,danceability,duration,energy,loudness,year,tempo,analysis_rate,end_of_fade_in,key,key_confidence,mode,mode_confidence,start_of_fade_out,time_signature,time_signature_conf,song_id")
    #csvfile.write("familiarity, hotttness")
    csvfile.write("\n")

    # Recursively visit each sub-dir till we reach the h5 files
    # Strip punctuation from features that are strings
    for root, dirs, filenames in os.walk(data_dir):
        for f in filenames:
            if f[-3:] != '.h5':
                continue
            #log = open(os.path.join(root, f),'r')
            #print os.path.join(root, f)

            # Use the hd5 wrappers to open the h5 file
            h5 = hdf5_getters.open_h5_file_read(os.path.join(root, f))

            # EXTRACTING FEATURES
            # See hd5_getter.py for the various features that we can extract from each h5 file
            #Get song id
            song_id = hdf5_getters.get_song_id(h5)
            if song_id not in songSet:
                continue

            # Get the artist name
            artist_name = hdf5_getters.get_artist_name(h5)
            artist = artist_name.translate(None, string.punctuation)


            # Get the title of the song
            title_song = hdf5_getters.get_title(h5)
            title = title_song.translate(None, string.punctuation)

            # Get artist location
            artist_location = hdf5_getters.get_artist_location(h5)
            artist_loc = artist_location.translate(None, string.punctuation)

            # Get release
            release_song = hdf5_getters.get_release(h5)
            release = release_song.translate(None, string.punctuation)

            # Get artist HOTTTNESSSSSS
            hotttness = hdf5_getters.get_artist_hotttnesss(h5)

            # Get artist familiarity
            familiarity = hdf5_getters.get_artist_familiarity(h5)

            # Get danceability
            danceability = hdf5_getters.get_danceability(h5)

            # Get duration
            duration = hdf5_getters.get_duration(h5)

            # Get energy
            #*****useless... column is filled with 0's?
            energy = hdf5_getters.get_energy(h5)

            # Get loudness
            loudness = hdf5_getters.get_loudness(h5)

            # Get year
            year = hdf5_getters.get_year(h5)

            # Get tempo
            tempo = hdf5_getters.get_tempo(h5)

            #########################################################

            # Get analysis sample rate
            analysis_rate = hdf5_getters.get_analysis_sample_rate(h5)

            # Get end of fade in
            end_of_fade_in = hdf5_getters.get_end_of_fade_in(h5)

            # Get key
            key = hdf5_getters.get_key(h5)

            # Get key confidence
            key_confidence = hdf5_getters.get_key_confidence(h5)

            # Get mode
            mode = hdf5_getters.get_mode(h5)

            # Get mode confidence
            mode_confidence = hdf5_getters.get_mode_confidence(h5)

            # Get start of fade-out
            start_of_fade_out = hdf5_getters.get_start_of_fade_out(h5)

            # Get time signature
            time_signature = hdf5_getters.get_time_signature(h5)

            # Get time signature confidence
            time_signature_conf = hdf5_getters.get_time_signature_confidence(h5)

            # Get track_id
            #track_id = hdf5_getters.get_track_id(h5)

            num_songs = hdf5_getters.get_num_songs(h5)

            #flush the table
            h5.flush()
            # Close the h5 file
            h5.close()
            tables.file._open_files.close_all()

            # Write to the CSV file
            csvfile.write(artist + "," + title + "," + artist_loc + "," + release + "," + str(hotttness) + "," + str(familiarity) + "," + str(danceability) + "," + str(duration) + "," + str(energy) + "," + str(loudness) + "," + str(year) + "," + str(tempo) + "," + str(analysis_rate) + "," + str(end_of_fade_in) + "," + str(key) + "," + str(key_confidence) + "," + str(mode) + "," + str(mode_confidence) + "," + str(start_of_fade_out) + "," + str(time_signature) + "," + str(time_signature_conf) + "," + str(song_id))
            #csvfile.write(str(familiarity) + "," + str(hotttness))
            csvfile.write("\n")

            # Print the current song and arists:
            print title + " by " + artist_name
            #print str(num_songs)
            # Move on to the next h5 file
            print
            print
