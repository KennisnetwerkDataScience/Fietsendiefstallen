# Auteur: Erik Duisterwinkel

import pandas as pd
import numpy as np
import numpy.matlib
import matplotlib.pyplot as plt
import math
from dateutil.parser import parse

# READ data
## diefstal data
df = pd.read_csv("fietsdata.csv", sep=';', encoding='iso-8859-1')
numitems = df['Begin-pleegdatum/tijd'].count()
## neighbourhood information (numbering used in first dataset)
buurten = pd.read_csv("buurtnummers.csv", sep=';', encoding='iso-8859-1', index_col='Buurtnummer')
## new dataframes for info on interval/window information
intervaldf = pd.DataFrame(np.zeros([numitems,2]), index=df.index.values, columns=['interval_start', 'interval_end'], dtype='uint8')
weightdf = pd.DataFrame(1.0*np.zeros([numitems,1]), index=df.index.values, columns=['weight'], dtype=np.float64)

# separate each incident per time interval
# give weight to each incident per time interval
# e.g. 1 incident reported over 4 hours means 4 times a 0.25 incident
for i in range(numitems):
    tdelta = parse(df['Eind-pleegdatum/tijd'][i])-parse(df['Begin-pleegdatum/tijd'][i])
    tdelta_hours = np.maximum(math.ceil(abs(tdelta.days*24 + tdelta.seconds/3600)),1)
    if tdelta_hours >= 24:
        # if more than 24 hours, assume equal distribution over whole day
        intervaldf['interval_start'][i] = 0
        intervaldf['interval_end'][i] = 23
        weightdf['weight'][i] = 1.0/24      # linear weight distribution
    else:
        intervaldf['interval_start'][i] = parse(df['Begin-pleegdatum/tijd'][i]).time().hour
        intervaldf['interval_end'][i] = intervaldf['interval_start'][i] + tdelta_hours
        weightdf['weight'][i] = 1.0/tdelta_hours      # linear weight distribution

df['interval_start'] = intervaldf['interval_start']
df['interval_end'] = intervaldf['interval_end']
df['weight'] = weightdf['weight']

# fill up array with neighbourhood versus timeinterval that counts incidents
incident_density = np.zeros([68, 24])
for i in range(numitems):
    if df['interval_start'][i] < df['interval_end'][i]:
        incident_density[ df['Buurtnummer'][i]-1 ][ df['interval_start'][i]:df['interval_end'][i]] = incident_density[ df['Buurtnummer'][i]-1 ][ df['interval_start'][i]:df['interval_end'][i]] + df['weight'][i]
    else:
        incident_density[df['Buurtnummer'][i] - 1][ 0:df['interval_eind'][i] ] = incident_density[ df['Buurtnummer'][i]-1][ 0:df[   'interval_eind'][i] ] + df['weight'][i]
        incident_density[df['Buurtnummer'][i] - 1][df['interval_start'][i]:23] = incident_density[df['Buurtnummer'][i]-1][df['interval_eind'][i]:23] + df['weight'][i]

# FIRST ORDER CORRECTION ON INCIDENT TIMING
## get average distribution over time
avg_distribution = incident_density.sum(axis=0)                 # sum incidents per time interval
avg_distribution = avg_distribution / avg_distribution.sum()    # normalize
incident_density_FO = np.zeros([68, 24])
## first order correct on weight distribution per incident
for i in range(numitems):
    num_interval = df['interval_end'][i]-df['interval_start'][i]
    weight = np.zeros([24,1])
    if df['interval_start'][i] < df['interval_end'][i]:
        weight[df['interval_start'][i]:df['interval_end'][i]] = 1
    else:
        weight[0:df['interval_end'][i]] = 1
        weight[df['interval_start'][i]:23] = 1

    weight = weight.T * avg_distribution      # correct for distribution
    weight = weight / weight.sum()          # normalize

    incident_density_FO[df['Buurtnummer'][i] - 1][:] = incident_density_FO[df['Buurtnummer'][i] - 1][:] + weight

# select only top 10 neighbourhoods
num_per_neighbourhood = np.matlib.sum(incident_density,1);  # count total number per neighbourhood
sel_neighbourhood = num_per_neighbourhood.argsort()[-10:]    # select neighbourhoods with largest total number
sel_neighbourhood = sel_neighbourhood[::-1]
show_data = incident_density[sel_neighbourhood][:]
show_data_FO = incident_density_FO[sel_neighbourhood][:]

# visualisation
t = np.matlib.repmat( np.arange(0,24,1).T, 10, 1)
plt.figure(1)
plt.plot(t.T, show_data.T)
plt.xlabel('tijdstip op de dag (uur)')
plt.ylabel('diefstal dichtheid (per wijk)')
plt.title('Diefstallen door de tijd (uren per dag)')
plt.grid(True)
plt.legend(buurten['Pleegsubbuurt'][sel_neighbourhood])
plt.xlim([0,23])
plt.ylim([0,1.05*np.max(np.amax(show_data))])
plt.show()

# visualisation FO (first order correction)
t = np.matlib.repmat( np.arange(0,24,1).T, 10, 1)
plt.figure(2)
plt.plot(t.T, show_data_FO.T)
plt.xlabel('tijdstip op de dag (uur)')
plt.ylabel('diefstal dichtheid (per wijk)')
plt.title('Diefstallen door de tijd* (uren per dag)')
plt.grid(True)
plt.legend(buurten['Pleegsubbuurt'][sel_neighbourhood])
plt.xlim([0,23])
plt.ylim([0,1.05*np.max(np.amax(show_data_FO))])
plt.show()


