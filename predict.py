# coding=gbk
import os

import numpy as np
import pandas as pd

import scipy.spatial.distance as ssd

from prototype import prototype
from dissimilarity import dissimilarity
from utils import up_sample, normalization

from sklearn.neighbors import NearestNeighbors


class Predictor(object):
    def __init__(self, data_type, data_time, thresh, pd):
        self.data_type = data_type
        self.data_time = data_time
        self.thresh = thresh
        self.positive = 1
        self.pd = pd
        # print('DATA TYPR:', self.data_type)
        self.DBR_X_train, self.Prototypes = self.get_model()
        self.X_test = self.preprocess()


    def preprocess(self):
        df = self.pd[self.data_type]

        df = up_sample(df, self.data_type, source_sample=self.data_time, dest_sample=200)

        df = normalization(df, method="max_min_scaler")
        # 保存序列
        a_list = [float(value) for value in df.values]
        assert len(a_list) == 200, "Data Dimension Error!"
        X_test = np.array(a_list)[np.newaxis, :]

        return X_test

    def postprocess(self):
        pass

    def get_model(self):
        # Save Prototypes
        data_type = self.data_type

        weights_path = os.path.join(os.getcwd(), 'weights', str(self.data_time), data_type)
        if not os.path.exists(weights_path):
            os.makedirs(weights_path)
        DBR_X_train = np.load(os.path.join(weights_path, 'DBR_X_train.npy'))
        Prototypes = np.load(os.path.join(weights_path, 'Prototypes.npy'))
        return DBR_X_train, Prototypes

    def predict(self):
        # SELECT DISS. MEASURE and PROTOTYPE METHOD
        D, P = dissimilarity(), prototype()

        Dissimilarity = D.kullback_leibler
        diss_params = {}

        DBR_X_test = ssd.cdist(self.X_test, self.Prototypes, Dissimilarity, **diss_params)

        Classifier = NearestNeighbors(n_neighbors=1)
        Classifier.fit(self.DBR_X_train)

        # print(Y_test, Classifier.kneighbors(DBR_X_test))

        predict_score = Classifier.kneighbors(DBR_X_test)[0]
        Y_pred = np.zeros_like(predict_score.squeeze())
        if predict_score.squeeze() < self.thresh:
            Y_pred = 1
        return int(Y_pred), predict_score.squeeze()


if __name__ == "__main__":
    csv_File = open("data/csv_data/test_negative_4.csv", 'r')  # 打开csv文件
    pd = pd.read_csv(csv_File)

    data_type_list = ['electricCurrent', 'activePower', 'apparentPower']
    thresh = [0.14927437, 0.11817348, 0.0900907]
    # , 'activePower', 'apparentPower'
    for i, data_type in enumerate(data_type_list):
        model = Predictor(
            data_type=data_type,
            data_time=30,
            thresh=thresh[i],
            pd=pd
        )
        y_pred, predict_score = model.predict()
        print("predict result: ", y_pred, predict_score)
