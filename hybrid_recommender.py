import pandas as pd
from colab_filtering import get_top_n
import content_model as cbm
import random
from surprise.prediction_algorithms.predictions import Prediction

class HybridRecommender:
    def __init__(self, cbm_model, scaler, user_database, song_database, features, predictions):
        self.cbm_model = cbm_model
        self.scaler = scaler
        self.user_database = user_database
        self.song_database = song_database
        self.features = features
        self.cf_predictions = predictions
        self.predictions_dict = {}
        self.actual_dict = {}

    def calculateHistory(self,user):
        return self.user_database[self.user_database['user'] == user].shape[0]

    def setUpPredictionsDict(self):
        for uid, iid, _, est, _ in self.cf_predictions:
            self.predictions_dict[(uid,iid)] = est
        print("done")

    def getListOfPredictions(self,user,recs_portion, mode='cf'):
        out_predictions = []
        cbm_value = self.user_database['plays'].mean()
        for iid in recs_portion:
            if self.user_database[(self.user_database['user'] == user) & (self.user_database['song'] == iid)].shape[0] == 0:
                actual_plays = 0
            else:
                actual_plays = self.user_database[(self.user_database['user'] == user) & (self.user_database['song'] == iid)]['plays'].iloc[0]
            if mode == 'cf':
                estimated_rating = self.predictions_dict[(user,iid)]
                out_predictions.append(Prediction(uid=user, iid=iid, r_ui=actual_plays, est=estimated_rating, details={}))
            else:
                estimated_rating = cbm_value
                out_predictions.append(Prediction(uid=user, iid=iid, r_ui=actual_plays, est=estimated_rating,details={}))

        return out_predictions


    def run(self):
        out_predictions = []
        print('setting up dict...')
        self.setUpPredictionsDict()
        i = 0
        for user in list(set(self.user_database['user'])):
            print('user:',i)
            i+=1
            hybrid_recs = None
            cf_recs = get_top_n(user, self.cf_predictions, n=10)
            print('got cf_recs')
            cbm_recs = cbm.top_n(user_id=user, n=10, model=self.cbm_model, scaler=self.scaler, user_database=self.user_database, song_database=self.song_database, features=self.features)
            print('got cbm_recs')
            history = self.calculateHistory(user)
            print('calculatedHistory')
            if history > 50:
                hybrid_recs = cf_recs
                out_predictions.extend(self.getListOfPredictions(user, hybrid_recs))
                print('got out_predictions')
            else:
                cf_sample = int(history / 5)
                cbm_sample = 10 - cf_sample
                cf_recs_portion = random.sample(cf_recs, cf_sample)
                cbm_recs_portion = random.sample(cbm_recs, cbm_sample)
                out_predictions.extend(self.getListOfPredictions(user, cf_recs_portion))
                out_predictions.extend(self.getListOfPredictions(user, cbm_recs_portion, mode='cbm'))
                print('got out_predictions')

        return out_predictions






