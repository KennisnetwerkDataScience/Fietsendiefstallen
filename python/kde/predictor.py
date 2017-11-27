#!/usr/bin/env python3
#used to create a simple predictor of the amount of thefts in a given period.
#Run script with -h to get more info.

from sklearn.neural_network import MLPRegressor
import matplotlib.pyplot as plt
from scipy import stats
import argparse
import logging
import glob

import matplotlib.pyplot as plt
from scipy.misc import imread
import matplotlib.cbook as cbook

import os

import pandas as pd

from datetime import datetime, timedelta

from rdwgs_converter import RDWGSConverter

import numpy as np

import numpy as np
from sklearn.svm import SVR


conv = RDWGSConverter()

#Modify depending on map and area used:
#TODO: Move somewhere to a common place.
min_lat = 53.1781
min_lon = 6.4952
max_lat = 53.2556
max_lon = 6.6363
    
min_x, min_y = conv.fromWgsToRd((min_lat, min_lon))
max_x, max_y = conv.fromWgsToRd((max_lat, max_lon))


def read_dataset(path):
    logging.info("Reading file: %s" % path)
    converters = {}
    df = pd.read_csv(path, sep=",", encoding="ISO-8859-1", converters=converters)
    return df


def main(args=None):
    parser = argparse.ArgumentParser(description='Create a bike theft predictor.')
    parser.add_argument('file', type=str, help='Path to dataset.')
    args = parser.parse_args(args)

    df = read_dataset(args.file)
    columns = df.columns.values
    logging.debug("Columns found: %s" % (str(columns)))

    #Convert df to dataset:
    y_train = []; y_test = []
    X_train = []; X_test = []
    l = len(df)
    for i, (k, r) in enumerate(df.iterrows()):
        fv = [r['bushaltes'], r['cameratoezicht_vlak'], r['coffeeshops'], r['horeca'], \
             r['onth_verg_drank_en_horeca'], r['openbareverlichting'], r['slaapopvang_en_methadon'], r['verblijfsobjecten']]
        if i < (l / 2):
            y_train.append(r["count"])
            X_train.append(fv)
        else:
            y_test.append(r["count"])
            X_test.append(fv)

    #Train:
    predictor = SVR(kernel='rbf', C=1e3, gamma=0.1).fit(X_train, y_train)
    #predictor = MLPRegressor((100,200,100)).fit(X_train, y_train)

    y_train_predicted = predictor.predict(X_train)
    y_test_predicted = predictor.predict(X_test)

    img = imread('osm_map.png')

    axes = plt.gca()
    axes.set_ylim([min_y,max_y])
    axes.set_xlim([min_x,max_x])

    max_v = 100
    R = []
    for r in range(30):
        row = []
        if r * 30 < len(y_train):
            for c in range(30):
                v = y_train_predicted[r * 30 + c]
                if v > max_v:
                    v = max_v
                row.append(v)
        else:
            for c in range(30):
                v = y_test_predicted[(r - 15) * 30 + c]
                if v > max_v:
                    v = max_v
                row.append(v)
        R.append(row)

    plt.imshow(img, zorder=0, extent=[min_x, max_x, min_y, max_y])
    plt.imshow(R, cmap=plt.cm.viridis, extent=[min_x, max_x, min_y, max_y], alpha=0.60)
    plt.show()

  

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    main()
