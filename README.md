# Project Name
Meteorite Landing Locations vs. Countries Today

## Purpose

There is a database that keeps where all the detectable meteorites have landed on Earth in all of history and tells us their geolocation, but it would be fun to know where these meteorites actually are in today's countries. For example, if my goal is to simply visit a country with the most number of meteorite landing sites, the way to get the best bang for the buck would be to look at which country in the present world has the most meteorite landing sites. This project allows us to do that in a friendly web interface based in Django.

## Data set

* [Meteorite Landings Dataset](https://data.nasa.gov/Space-Science/Meteorite-Landings/gh4g-9sfh)
* [Meteorite Class Lookup](https://www.lpi.usra.edu/meteor/metbullclass.php)
* [Today's Countries](https://unstats.un.org/unsd/methodology/m49/)

## Data model

![](/static/img/data_model.png)

## Package Dependencies

Please see [requirements.txt](/requirements.txt)

## Notes

- the sql file in ```static/sql``` has a ```.txt``` suffix that would have to be removed to execute the script. It's there because I've included ```*.sql``` in my ```.gitignore```.

- When executing the sql script, there may be warning messages about data being truncated when importing the data locally, I've double checked, the data is imported correctly despite the warning

- I've written a couple of python scripts that preprocessed the data in ```scripts/input/csv``` [meteorite_class.py](scripts/input/csv/meteorite_classes.py) and [meteorite_landings_alter.py](scripts/input/csv/meteorite_landings_alter.py).

- There are 3 List Views: **country/area**, **meteorite class**, and **meteorite landing** (using association table that links country/area and meteorite class). **Meteorite landing** is needed because it also contains some information such as the number of meteorites that have fallen in that country, average mass, etc.

- There are 2 edit forms. One for **Meteorite Class** which will allow for changing definition, and countries it is linked to (which generates entries for Meteorite Landings ListView), the other one is **Meteorite Landing** which will allow for changing **meteorite count**, **average mass**, **max mass**, **min mass**
