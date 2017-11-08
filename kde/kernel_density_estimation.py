#!/usr/bin/env python3

import argparse
import logging

import pandas as pd

from rdwgs_converter import RDWGSConverter


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


def main(args=None):
    parser = argparse.ArgumentParser(description='Applies and visualizes the kernel density estimation applied to the bike thefts.')
    parser.add_argument('file', help='Path the the bike theft file in tsv format.', type=str)
    parser.add_argument('--write_file', type=str, default=None, help='Writes the specified file after reading (and possibly conversion).')
    args = parser.parse_args(args)

    logging.info("Reading file: %s" % args.file)
    df = read_tsv(args.file)
    if not args.write_file is None:
        df.to_csv(args.write_file, sep="\t")


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    main()
