import content_model

def main():
	#####Build the Song Dataset, needed for KNN
	print("Building Song Dataset")
	
	#adjustable parameters below
	path = 'C:/Users/wyndh/OneDrive/Desktop/CSE6240_Project/data/output_usersong_features.csv'
	features = None #will default to ['hotttness','familiarity','duration','loudness','tempo','key','mode','time_signature']
	scaler = None #will default to RobustScaler
	
	train_data_norm, song_database, features, scaler = content_model.build_song_dataset(filepath=path, features=features, scaler=scaler)



	######Build the User Dataset, used to find songs and playcounts for given user_id
	print("Building the User Database")

	#adjustable parameters below
	path_user = 'C:/Users/wyndh/OneDrive/Desktop/CSE6240_Project/data/train_triplets.txt'

	user_database = content_model.build_user_dataset(path_user)



	######Build the actual model itself
	print("Building the KNN model on the training data")

	#adjustable parameters below
	K = 1000 #number of nearest neighbors
	dist_metric = 'manhattan' #options are at https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.DistanceMetric.html

	model = content_model.build_model(train_data_norm,k=K,dist_metric=dist_metric)


	###### Run on a user
	print("Running on a user")

	#adjustable parameters (remaining parameters should be taken from the setup functions)
	n = 30
	user_id = '3f61ead20ef5d0c5d31256ed703228e6f7e1c540'
	recommended_songs = content_model.top_n(user_id=user_id, n=n, model=model, scaler=scaler, user_database=user_database, song_database=song_database, features=features)

	print(user_id)
	print(recommended_songs)


if __name__ == "__main__":
	main()
