import matplotlib.pyplot as plt
import pandas as pd
from surprise import Dataset, Reader
from surprise import SVD
from surprise.model_selection import train_test_split
from collections import defaultdict

data = pd.read_csv('train_triplets.txt', sep="\t", header=None)
data.columns = ['user', 'song', 'plays']
data = data[:30000]

song_df =  pd.read_csv('song_data.csv')
data_surprise = Dataset.load_from_df(data, Reader(rating_scale=(1, data['plays'].max())))
# trainset, testset = train_test_split(data_surprise, test_size=.25)

trainset = data_surprise.build_full_trainset()
svd = SVD()
svd.fit(trainset)

testset = trainset.build_anti_testset()
predictions = svd.test(testset)

def get_top_n(user_id, n=10):
    '''Return the top-N recommendation for user from a set of predictions.

    Args:
        user_id: User ID
        n(int): The number of recommendation to output for each user. Default
            is 10.

    Returns:
    A list of dictionaries: {title, artist, year}
    '''
    top_n = defaultdict(list)
    for uid, iid, _, est, _ in predictions:
        if uid == user_id:
            top_n[uid].append((iid, est))

    # Then sort the predictions for each user and retrieve the k highest ones.
    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = user_ratings[:n]

    recommendations = []
    for uid, user_ratings in top_n.items():
        for rating in user_ratings:
            song_id = rating[0]
            song_title = song_df[song_df['song_id'] == song_id]['title'].to_string().split('    ')[1]
            artist = song_df[song_df['song_id'] == song_id]['artist_name'].to_string().split('    ')[1]
            year = song_df[song_df['song_id'] == song_id]['year'].to_string().split('    ')[1]
            recommendations.append({'title': song_title, 'artist': artist, 'year': year})

    return recommendations

# user_id = 'b80344d063b5ccb3212f76538f3d9e43d87dca9e'
# user_id = '8caf9a87e266a22298bd977a63489d008af241c5'
# rec = get_top_n(user_id, n=10)
# print(rec)
