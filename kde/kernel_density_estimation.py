#!/usr/bin/env python3

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

min_lat = 53.2068
max_lon = 6.5930

max_lat = 53.2276
min_lon = 6.5417

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


def sub_plot(df, title=None, save_image=None):
    plt.clf()

    #plt.figure(figsize=(1920 / 200.0, 1080 / 200.0))

    img = imread('osm_map.png')
    plt.scatter(df["x"],df["y"],zorder=1, c='r', s=1)

    axes = plt.gca()
    axes.set_ylim([min_y,max_y])
    axes.set_xlim([min_x,max_x])

    X, Y = np.mgrid[min_x:max_x:100j, min_y:max_y:100j]
    positions = np.vstack([X.ravel(), Y.ravel()])
    values = np.vstack([df["x"], df["y"]])
    #kernel = stats.gaussian_kde(values, bw_method=0.15)
    kernel = stats.gaussian_kde(values)
    Z = np.reshape(kernel(positions).T, X.shape)

    if not title is None:
        plt.title(title)

    plt.imshow(img, zorder=0, extent=[min_x, max_x, min_y, max_y])
    plt.imshow(np.rot90(Z), cmap=plt.cm.Reds, extent=[min_x, max_x, min_y, max_y], alpha=0.70)
    if save_image is None:
        plt.show()
    else:
        plt.savefig(save_image)



def plot(df):
    start_dt       = to_date("2013-01-01T00:00:00Z")
    end_dt         = to_date("2017-09-01T00:00:00Z")
    window         = timedelta(days=100)
    window_overlap = timedelta(days=1)
    cur_dt         = start_dt
    
    count = 0
    while cur_dt < end_dt:
        cur_dt_str = cur_dt.strftime("%Y-%m-%dT%H:%M:%S")
        cur_dt_end_str = (cur_dt + window).strftime("%Y-%m-%dT%H:%M:%S")
        range_str = "%s - %s" % (cur_dt_str, cur_dt_end_str)
        logging.info("Range: %s" % range_str)

        subdf = df[df['begin_pleegdatumtijd'] > cur_dt_str]
        subdf = subdf[df['begin_pleegdatumtijd'] < cur_dt_end_str]

        sub_plot(subdf, title=range_str, save_image="output/%04d.png" % count)

        cur_dt += window_overlap
        count += 1


    #for k, s in df.iterrows():
    #    print(s["begin_pleegdatumtijd"])


def main(args=None):
    parser = argparse.ArgumentParser(description='Applies and visualizes the kernel density estimation applied to the bike thefts.')
    parser.add_argument('file', help='Path the the bike theft file in tsv format.', type=str)
    parser.add_argument('--write_file', type=str, default=None, help='Writes the specified file after reading (and possibly conversion).')
    args = parser.parse_args(args)

    logging.info("Reading file: %s" % args.file)
    df = read_tsv(args.file)
    if not args.write_file is None:
        df.to_csv(args.write_file, sep="\t")

    #df = df[df['begin_pleegdatumtijd'].hour > 0]
    for i in range(24):
        subdf = df[pd.DatetimeIndex(df['begin_pleegdatumtijd']).hour == i]
        #subdf = subdf[pd.DatetimeIndex(subdf['begin_pleegdatumtijd']).hour < (i + 1)]
        print("LEN: %d" % len(subdf))
        if len(subdf) > 0:
            sub_plot(subdf, title="hour: %d" % i)

    #df = df[df['begin_pleegdatumtijd'] > "T12:00:00"]
    #df = df[df['begin_pleegdatumtijd'].between_time('20:00', '22:00')]
    #df = df.set_index('begin_pleegdatumtijd')
    #df = df['begin_pleegdatumtijd'].between_time('20:00', '22:00')
    #df = df['begin_pleegdatumtijd'].between_time('20:00', '22:00')
    print(len(df))
    #plot(df)


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    main()
