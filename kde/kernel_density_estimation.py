#!/usr/bin/env python3

from scipy import stats
import argparse
import logging

import pandas as pd

from rdwgs_converter import RDWGSConverter

import numpy as np
import matplotlib.pyplot as plt
from scipy.misc import imread
import matplotlib.cbook as cbook


conv = RDWGSConverter()

min_lat = 53.2068
max_lon = 6.5930
min_x, min_y = conv.fromWgsToRd((min_lat, max_lon))

max_lat = 53.2276
min_lon = 6.5417
max_x, max_y = conv.fromWgsToRd((max_lat, min_lon))


def read_tsv(path):
    converters = {}
    df = pd.read_csv(path, sep="\t", encoding="ISO-8859-1", converters=converters)

    columns = df.columns.values
    logging.debug("Columns found: %s" % str(columns))
    if not ("lat" in columns and "lon" in columns):
        conv = RDWGSConverter()
        def convert(x, y):
            return conv.fromRdToWgs((x, y))
        df["lat"], df["lon"] = convert(df["x"], df["y"])
    return df


def plot(df):
    #np.random.seed(0)
    #x = np.random.uniform(0.0,10.0,15)
    #y = np.random.uniform(0.0,10.0,15)

    datafile = 'osm_map.png'
    img = imread(datafile)
    #plt.scatter([],[],zorder=1)
    plt.scatter(df["x"],df["y"],zorder=1)

    axes = plt.gca()
    axes.set_ylim([min_y,max_y])
    axes.set_xlim([min_x,max_x])

    X, Y = np.mgrid[min_x:max_x:100j, min_y:max_y:100j]
    positions = np.vstack([X.ravel(), Y.ravel()])
    values = np.vstack([df["x"], df["y"]])
    kernel = stats.gaussian_kde(values)
    Z = np.reshape(kernel(positions).T, X.shape)

    plt.imshow(img, zorder=0, extent=[min_x, max_x, min_y, max_y])
    plt.imshow(np.rot90(Z), cmap=plt.cm.gist_earth_r, extent=[min_x, max_x, min_y, max_y], alpha=0.5)
    #plt.imshow(img, zorder=0)
    #plt.imshow(img, zorder=0)
    plt.show()


def main(args=None):
    parser = argparse.ArgumentParser(description='Applies and visualizes the kernel density estimation applied to the bike thefts.')
    parser.add_argument('file', help='Path the the bike theft file in tsv format.', type=str)
    parser.add_argument('--write_file', type=str, default=None, help='Writes the specified file after reading (and possibly conversion).')
    args = parser.parse_args(args)

    logging.info("Reading file: %s" % args.file)
    df = read_tsv(args.file)
    if not args.write_file is None:
        df.to_csv(args.write_file, sep="\t")

    plot(df)


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    main()
