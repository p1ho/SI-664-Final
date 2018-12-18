# Requires: "meteorite_landings.csv"
#
# This script takes all the possible meteorite types, and run it against a web
# service to get full_name/definition, then store it in a csv.
#
# It will generate "meteorite_classes.csv"
#
# Notes:
# - Meteorites that are the following will be skipped:
#   1) Location undocumented (blank/(0,0))
#   2) Mass undocumented

import time
import csv
import json
import requests as req
from bs4 import BeautifulSoup as bs

def main():

    csv_enc = 'utf-8'
    csv_fname = 'meteorite_landings.csv'
    meteor_data = open(csv_fname, 'r', encoding=csv_enc)
    meteor_data_reader = csv.reader(meteor_data)
    next(meteor_data_reader)

    # tally meteorite classes
    meteor_class_set = set()
    for row in meteor_data_reader:
        mass = row[4]
        lat = row[7]
        lng = row[8]
        if lat != '0' and lat != "" and lng != '0' and lng != "" and mass != "":
            meteor_class = row[3].strip()
            meteor_class_set.add(meteor_class)
    meteor_data.close()

    # try to open cache
    cache_name = 'meteorite_classes_cache.json'
    try:
        file = open(cache_name, 'r')
        cache = json.loads(file.read())
        file.close()
        has_cache = True
        print('Cache found!')
    except:
        cache = {}
        has_cache = False
        print('Cache Not found, refetching data!')

    meteor_class_dict = {}
    print('There are {} classes needed.'.format(len(meteor_class_set)))
    count = 1
    for meteor_class in meteor_class_set:
        if has_cache == False or meteor_class not in cache.keys():
            print('Fetching class {}: {}'.format(count, meteor_class))
            time.sleep(.2) # prevent ip from being blocked
            url = 'https://www.lpi.usra.edu/meteor/metbullclass.php'
            params = {'sea': meteor_class}
            html = req.get(url, params=params)
            cache[meteor_class] = html.text
        else:
            print('Fetching class {} from Cache: {}'.format(count, meteor_class))
        soup = bs(cache[meteor_class], 'html.parser')
        soup_paragraphs = soup.find_all('p', attrs={'style': "margin-left: 0.5in"})
        definition = sanitize_text(soup_paragraphs[0].text)
        if len(soup_paragraphs) <= 1:
            description = "N/A"
        else:
            # website has a bug where p tags are not closed properly (<p> instead of </p>)
            # There is usually a link at the end that says "Find all meteorites of type: "
            # We must remove it
            text_to_remove = soup.find_all('p')[-1].text
            description = []
            for i in range(1, len(soup_paragraphs)):
                description.append(sanitize_text(soup_paragraphs[i].text\
                                                .replace(text_to_remove, '')))
            meteor_class_dict[meteor_class] = {\
                'definition' : definition,\
                'description' : description\
            }
            count += 1

    # save cache
    file = open(cache_name, 'w')
    file.write(json.dumps(cache))
    file.close()
    print('cache saved!')

    # build csv
    print('Building CSV')
    f_out = open('meteorite_classes.csv', 'w', encoding=csv_enc)
    f_out.write(u'"class_code"\t"definition"\t"description"\t\r\n')
    for meteor_class in meteor_class_dict:
        f_out.write(u'"{}"\t"{}"\t"{}"\t\r\n'.format(\
            meteor_class,\
            meteor_class_dict[meteor_class]['definition'],\
            ''.join(meteor_class_dict[meteor_class]['description'])\
        ))
    f_out.close()

def sanitize_text(s):
    return s.replace('\t',' ')\
            .replace('"',"'")\
            .replace('\n\n', '\n')\
            .replace('\n','<br><br>')\

if __name__ == '__main__':
	main()
