import sys
import os
from os import path
import geopandas as gpd


DATA = '../data'


skipfiles = ['fietsdiefstallen_met_buurtnummers.zip']
specialfiles = dict(
    cameratoezicht_akwartier=['cameratoezicht_lijn', 'cameratoezicht_vlak'],
    diefstallen_met_afstanden=['diefstallen_afstanden']
)
files = [path.join(DATA, f) for f in os.listdir(DATA) if f not in skipfiles]
zipfiles = ['../data/horeca.zip']  # for testing
zipfiles = [f for f in files if path.isfile(f) and f.endswith('.zip')]

for filename in zipfiles:
    name = path.splitext(path.basename(filename))[0]
    print('processing %s' % name)
    sources = specialfiles[name] if name in specialfiles else [name]
    for src in sources:
        gdf = gpd.read_file('/%s.shp' % src, vfs='zip://%s' % filename)
        gdf['x'] = gdf['geometry'].centroid.x
        gdf['y'] = gdf['geometry'].centroid.y
        gdf.to_csv('%s.csv' % src)
