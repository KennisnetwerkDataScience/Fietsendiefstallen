#!/usr/bin/env python3

import argparse
import logging

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
        self._grid_features = {c:{"count":0, "lights":0} for c in range(grid * grid)}
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

    def add_lights(self, df):
        logging.info("Adding %d lights." % len(df))
        for k, r in df.iterrows():
            x, y = self._conv.fromWgsToRd((r["y"], r["x"]))
            cel = self.to_cel_index(x, y)
            #Add if cel is not outside grid:
            if not cel is None:
                self._grid_features[cel]["lights"] += 1

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
    parser.add_argument('--lights', type=str, default=None, help='If set, uses the specified file to append light information to the dataset.')
    parser.add_argument('--grid', type=int, default=30, help='If set uses the specified value as the widht/height of the grid to assign the rows to.')
    args = parser.parse_args(args)

    df = read_theft_tsv(args.file)

    e = GridFeatureExtractor(args.grid)
    e.set_y(df)
    if not args.lights is None:
        lights_df = pd.read_csv(args.lights, sep=",", encoding="ISO-8859-1")
        columns = lights_df.columns.values
        logging.debug("Light columns found: %s" % str(columns))
        e.add_lights(lights_df)
    print(e.get_features())


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    main()
