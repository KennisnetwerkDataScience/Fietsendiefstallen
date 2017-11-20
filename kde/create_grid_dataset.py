#!/usr/bin/env python3

import argparse
import logging
import glob

import os

import pandas as pd

from datetime import datetime, timedelta

from rdwgs_converter import RDWGSConverter

import numpy as np


conv = RDWGSConverter()

small = False
if small:
    min_lat = 53.2068
    max_lon = 6.5930
    max_lat = 53.2276
    min_lon = 6.5417
else:
    min_lat = 53.1781
    min_lon = 6.4952
    max_lat = 53.2556
    max_lon = 6.6363

    
min_x, min_y = conv.fromWgsToRd((min_lat, min_lon))
max_x, max_y = conv.fromWgsToRd((max_lat, max_lon))


def read_theft_tsv(path):
    logging.info("Reading file: %s" % path)
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


class GridFeatureExtractor():

    def __init__(self, grid):
        self._grid = grid
        self._cel_max = grid * grid - 1
        self._grid_features = {c:{"count":0} for c in range(grid * grid)}
        self._box_width = (max_x - min_x) / self._grid
        self._box_height = (max_y - min_y) / self._grid
        self._conv = RDWGSConverter()

    def to_cel_index(self, x, y):
        """ Returns the index of the grid cel providing the x and y coordinates. """
        x_pos = int((x - min_x) / self._box_width)
        y_pos = int((y - min_y) / self._box_height)
        index = y_pos * self._grid + x_pos
        return None if index > self._cel_max else index

    def set_y(self, df):
        for k, r in df.iterrows():
            cel = self.to_cel_index(r["x"], r["y"])
            self._grid_features[cel]["count"] += 1

    def add_xy_count(self, df, name):
        logging.info("Adding %d of type %s." % (len(df), name))
        #Init:
        for c, fs in self._grid_features.items():
            fs[name] = 0
        #Count:
        for k, r in df.iterrows():
            x, y = self._conv.fromWgsToRd((r["y"], r["x"]))
            cel = self.to_cel_index(x, y)
            #Add if cel is not outside grid:
            if not cel is None:
                self._grid_features[cel][name] += 1

    def add_csv(self, csv_path):
        df = pd.read_csv(csv_path, sep=",", encoding="ISO-8859-1")
        columns = df.columns.values
        logging.debug("Columns found in %s: %s" % (csv_path, str(columns)))
        self.add_xy_count(df, os.path.basename(csv_path).split(".")[-2])

    def to_csv(self):
        #TODO: Use pandas for this?
        csv = ""
        cols = None
        for i in range(self._grid * self._grid):
            fs = self._grid_features[i]
            if cols is None:
                cols = list(fs.keys())
                cols.sort()
                cols.remove("count")
                csv += "cel,count"
                for c in cols:
                    csv += ",%s" % c
                csv += "\n"
            csv += "%d,%d" % (i, fs["count"])
            for c in cols:
                csv += ",%d" % fs[c]
            csv += "\n"
        return csv
            


    def get_features(self):
        return self._grid_features


def assign_grid(df, grid):
    assert grid in range(1, 100), "Invalid grid width/height specified!"
    box_width = (max_x - min_x) / grid
    box_height = (max_y - min_y) / grid
    def convert(x, y):
        x_pos = ((x - min_x) / box_width).astype(int)
        y_pos = ((y - min_y) / box_height).astype(int)
        return y_pos * grid + x_pos
    df["grid_%d" % grid] = convert(df["x"], df["y"])
    return df



def main(args=None):
    parser = argparse.ArgumentParser(description='Create a dataset suitable for regression proving the csvs.')
    parser.add_argument('file', type=str, help='Path to the bike theft file in tsv format.')
    parser.add_argument('--csvs', type=str, default=None, help='Path with csvs to calculate the features for.')
    parser.add_argument('--grid', type=int, default=30, help='If set uses the specified value as the widht/height of the grid to assign the rows to.')
    args = parser.parse_args(args)

    df = read_theft_tsv(args.file)

    e = GridFeatureExtractor(args.grid)
    e.set_y(df)

    for csv in glob.glob("%s/*.csv" % args.csvs):
        e.add_csv(csv)
    print(e.to_csv())
       

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    main()
