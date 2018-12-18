# Requires: "meteorite_landings.csv"
#
# This script converts geolocations from lat/lng to country, and aggregate data
# (only keeping count of meteorite by classes, and group by countries)
#
# It will generate "meteorite_types.csv"
#
# Notes:
# - Meteorites that are the following will be skipped:
#   1) Location undocumented (blank/(0,0))
#   2) Mass undocumented

import csv
import reverse_geocoder as rg
import numpy as np
import pycountry

def main():
    csv_fname = 'meteorite_landings.csv'
    csv_enc = 'utf-8'

    meteor_data = open(csv_fname, 'r', encoding=csv_enc)
    meteor_data_reader = csv.reader(meteor_data)
    next(meteor_data_reader)

    data_list = [] # where usable data are temporarily stored
    geolocation_list = [] #the list that will be passed to reverse_geocoder
    location_list = [] # using a list and not set because order is important
    for row in meteor_data_reader:
        meteor_class = row[3].strip().replace('\t', ' ')
        meteor_mass = row[4]
        lat = row[7]
        lng = row[8]
        if lat != '0' and lat != "" and lng != '0' and lng != "" and meteor_mass != "":
            meteor_mass = float(''.join(meteor_mass.split(',')))
            lat_rnd = round(float(lat), 1)
            lng_rnd = round(float(lng), 1)
            data_list.append({\
                'mass': meteor_mass,\
                'class': meteor_class,\
                'lat': lat_rnd,\
                'lng': lng_rnd
            })
            lat_lng_str = ', '.join([str(lat_rnd), str(lng_rnd)])
            if lat_lng_str not in location_list:
                location_list.append(lat_lng_str)
                geolocation_list.append((lat_rnd, lng_rnd))
            else:
                continue

    # mode 2 is faster but it's not stable on windows
    geolocation_reversed = rg.search(tuple(geolocation_list), mode=1)
    location_dict = {}
    for i in range(len(geolocation_reversed)):
        lat_lng_str = location_list[i]
        iso2 = geolocation_reversed[i]['cc']
        country = pycountry.countries.get(alpha_2=iso2).alpha_3
        location_dict[lat_lng_str] = country


    meteor_dict = {}
    for data in data_list:
        meteor_class = data['class']
        meteor_mass = data['mass']
        lat_lng_str = ', '.join([str(data['lat']), str(data['lng'])])
        # because there was already a first iteration, we know this look up will work
        country = location_dict[lat_lng_str]
        if country in meteor_dict:
            if meteor_class in meteor_dict[country]:
                meteor_dict[country][meteor_class].append(meteor_mass)
            else:
                meteor_dict[country][meteor_class] = [meteor_mass]
        else:
            meteor_dict[country] = {meteor_class: [meteor_mass]}

    # rebuild csv with data in meteor_dict
    f_out = open('meteorite_landings_alter.csv', 'w', encoding=csv_enc)
    f_out.write(u'"country_code"\t"meteorite_class"\t"count"\t"average_mass"\t"max_mass"\t"min_mass"\t\r\n')
    for country in meteor_dict:
        for meteor_class in meteor_dict[country]:
            meteor_tally = meteor_dict[country][meteor_class]
            f_out.write(u'"{}"\t"{}"\t"{}"\t"{}"\t"{}"\t"{}"\t\r\n'.format(\
                sanitize_text(country),\
                sanitize_text(meteor_class),\
                len(meteor_tally),\
                round(np.mean(meteor_tally), 2),\
                np.amax(meteor_tally),\
                np.amin(meteor_tally)\
            ))
    f_out.close()

def sanitize_text(s):
    return s.replace('\t',' ')\
            .replace('"',"'")\
            .replace('\n\n', '\n')\
            .replace('\n','<br><br>')\

if __name__ == '__main__':
	main()
