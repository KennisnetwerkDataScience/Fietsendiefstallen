#!/usr/bin/env python3
#File used to calculate the Kernel Density Estimation of the city.
#Run script with -h to get more info.

from scipy import stats
import argparse
import logging

import pandas as pd


from datetime import datetime, timedelta

from rdwgs_converter import RDWGSConverter

import numpy as np
import matplotlib.pyplot as plt
from scipy.misc import imread
import matplotlib.cbook as cbook


conv = RDWGSConverter()

#Modify depending on map and area used:
#TODO: Move somewhere to a common place.
min_lat = 53.1781
min_lon = 6.4952
max_lat = 53.2556
max_lon = 6.6363


min_x, min_y = conv.fromWgsToRd((min_lat, min_lon))
max_x, max_y = conv.fromWgsToRd((max_lat, max_lon))


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


def to_date(datestr):
    return datetime.strptime(datestr, '%Y-%m-%dT%H:%M:%SZ')


def plot_kde(df, title=None, save_image=None, pre_Z=None, only_calc=False):
    """ Calculates the Kernel Density Estimation and plots it result for the given dataframe. """ 
    plt.clf()

    #plt.figure(figsize=(1920 / 200.0, 1080 / 200.0))

    img = imread('osm_map.png')
    plt.scatter(df["x"],df["y"],zorder=1, c='r', s=0.5)

    axes = plt.gca()
    axes.set_ylim([min_y,max_y])
    axes.set_xlim([min_x,max_x])

    res = 50j
    X, Y = np.mgrid[min_x:max_x:res, min_y:max_y:res]
    positions = np.vstack([X.ravel(), Y.ravel()])
    values = np.vstack([df["x"], df["y"]])
    #kernel = stats.gaussian_kde(values, bw_method=0.15)
    kernel = stats.gaussian_kde(values)
    orig_Z = np.reshape(kernel(positions).T, X.shape)

    Z = orig_Z if pre_Z is None else orig_Z - pre_Z
    print(Z)

    if not title is None:
        plt.title(title)

    if not only_calc:
        plt.imshow(img, zorder=0, extent=[min_x, max_x, min_y, max_y])
        plt.imshow(np.rot90(Z), cmap=plt.cm.viridis, extent=[min_x, max_x, min_y, max_y], alpha=0.60)
        if save_image is None:
            plt.show()
        else:
            plt.savefig(save_image)
    return orig_Z



def sliding_window_plot(df, window_size=100, method="normal"):
    """ Plots and saves all results of the KDE using a sliding window. 
    window_size -- The size of the window to use in days.
    method      -- The method being used, can be any of:
                normal:      Just slides the window in time.
                diff:        The difference of the current window with the inital window at the start.
                diff_double: Similar to diff but in this case the initial window slides with the preceding window.
    """
    assert method in ["normal", "diff", "diff_double"]
    start_dt       = to_date("2013-01-01T00:00:00Z")
    end_dt         = to_date("2017-09-01T00:00:00Z")
    window         = timedelta(days=window_size)
    window_overlap = timedelta(days=1)
    cur_dt         = start_dt
    
    count = 0
    initial_Z = None
    while cur_dt < end_dt:
        cur_dt_str              =                  cur_dt.strftime("%Y-%m-%dT%H:%M:%S")
        cur_dt_end_str          =       (cur_dt + window).strftime("%Y-%m-%dT%H:%M:%S")
        cur_dt_double_end_str   = (cur_dt + (2 * window)).strftime("%Y-%m-%dT%H:%M:%S")
        range_str = "%s - %s" % (cur_dt_str, cur_dt_end_str)
        logging.info("Range: %s" % range_str)

        subdf = df[df['begin_pleegdatumtijd'] >= cur_dt_str]
        subdf = subdf[df['begin_pleegdatumtijd'] < cur_dt_end_str]

        if method == "normal":
            plot_kde(subdf, title=range_str, save_image="output/%04d.png" % count)
        elif method == "diff":
            Z = plot_kde(subdf, title=range_str, save_image="output/%04d.png" % count, pre_Z=initial_Z)
            if initial_Z is None:
                initial_Z = Z
        elif method == "diff_double":
            if cur_dt + window > end_dt:
                break
            Z = plot_kde(subdf, only_calc=True)
            if not Z is None:
                subdf = df[df['begin_pleegdatumtijd'] >= cur_dt_end_str]
                subdf = subdf[df['begin_pleegdatumtijd'] < cur_dt_double_end_str]
                plot_kde(subdf, title=range_str, save_image="output/%04d.png" % count, pre_Z=Z)

        cur_dt += window_overlap
        count += 1


def main(args=None):
    parser = argparse.ArgumentParser(description='Applies and visualizes the kernel density estimation applied to the bike thefts using a sliding window.')
    parser.add_argument('file', help='Path the the bike theft file in tsv format.', type=str)
    parser.add_argument('--method', type=str, default="normal", help='The method to use for the sliding window.')
    parser.add_argument('--window_size', type=int, default=100, help='The window size used for visualization in days.')
    parser.add_argument('--write_file', type=str, default=None, help='Writes the specified file after reading (and possibly conversion).')
    args = parser.parse_args(args)

    logging.info("Reading file: %s" % args.file)
    df = read_tsv(args.file)
    if not args.write_file is None:
        df.to_csv(args.write_file, sep="\t")

    if args.method == "full":
        plot_kde(df, title="KDE of whole dataset.")
    else:
        sliding_window_plot(df, args.window_size, args.method)


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    main()
