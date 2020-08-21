import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
import sklearn.preprocessing as preprocessing
from sklearn.model_selection import train_test_split


def build_song_dataset(filepath='data//output_usersong_features.csv', features=None, scaler=None):


	#import data as csv
	spotify_data = pd.read_csv(filepath, header=0)

	#default duplicate removal
	spotify_data_df = spotify_data.drop_duplicates()

	#clear songs with same IDs
	spotify_data_df = spotify_data.drop_duplicates(subset=['song_id'])

	#specified factors that we might care about
	spotify_data_df = spotify_data_df.dropna(axis=0,subset=['hotttness','familiarity','loudness','tempo','key','key_confidence','mode','mode_confidence'])

	#reset the index
	spotify_data_df = spotify_data_df.reset_index(drop=True)


	#set up train data
	train_data = None

	if features is None:
		#using default features that Pranshu wanted
		features = ['hotttness','familiarity','duration','loudness','tempo','key','mode','time_signature']
		train_data = spotify_data_df[features]
	else:
		train_data = spotify_data_df[features]


	train_data_norm = None

	if scaler is None:
		scaler = preprocessing.RobustScaler()
		train_data_norm = scaler.fit_transform(train_data)
	else:
		train_data_norm = scaler.fit_transform(train_data)

	return train_data_norm, spotify_data_df, features, scaler


def build_user_dataset(filepath='data//train_triplet.txt'):
	user_database = pd.read_csv(filepath, sep="\t",header=None)
	user_database.columns=['user','song','plays']
	return user_database



def build_model(train_data_norm,k=1000,dist_metric='manhattan'):
	model = NearestNeighbors(k, metric=dist_metric)
	model.fit(train_data_norm)
	return model


def top_n(user_id,model,scaler,user_database,song_database, features,n=100):
    #get all songs for this specific user
	user_i_data = user_database.loc[user_database['user'] == user_id]
	#check if user in dataset
	if len(user_i_data) == 0:
		raise Exception('User: {} has no songs'.format(user_id))

	#create a list of all the songs that this user listens to
	user_i_songs = user_i_data['song'].unique().tolist()

	total_playcount = user_i_data['plays'].sum()

	recommended_songs = []

	for song in user_i_songs:
		song_data = song_database.loc[song_database['song_id']==song]
		rel_song_data = song_data[features]
		scaled_song_data = scaler.transform(rel_song_data)
		neigh_ind = model.kneighbors(scaled_song_data, return_distance=False)

		#proportion of songs to add based on this song's playcount out the total playcount
		s_playcount = int(user_i_data.loc[user_i_data['song']==song,'plays'].iloc[0])
		end_index = max(int(1 + round(n*s_playcount/total_playcount)),2)

		#note that the first distance should be the song itself, so we start at index 1
		top_songs = neigh_ind[0][1:end_index]

		#find song ids and convert to list
		top_song_ids = song_database.iloc[top_songs,:][['song_id']]
		nearest_n_list = top_song_ids['song_id'].tolist()

		#add the closest songs for this song to the list
		recommended_songs.extend(nearest_n_list)

		'''
		display(song_data)
		print("------------------")
		display(song_database.iloc[top_songs,:])
		print("========================")
		'''

	if len(recommended_songs) > n:
		recommended_songs = np.random.choice(recommended_songs, n, replace=False)
		recommended_songs = list(recommended_songs)

	return recommended_songs
