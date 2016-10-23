import csv
from geojson import Point, Feature, FeatureCollection, dump
import re


def read_csv(fichier):
    with open(fichier, 'r', newline='') as f:
        reader = csv.DictReader(f, delimiter=';')

        return list(reader)


CHIFFRE_RE = re.compile(r'^-?[0-9.,]+$')


def coordonnees_correctes(c):
    return CHIFFRE_RE.match(c['longitude']) and CHIFFRE_RE.match(c['latitude'])


def extraire_coordonnees(communes):
    return {
        c['code_insee']: (
            float(c['longitude'].replace(',', '.')),
            float(c['latitude'].replace(',', '.'))
        ) for c in communes if coordonnees_correctes(c)
        }


if __name__ == "__main__":
    elevages = read_csv('data/elev.csv')
    communes = read_csv('data/eucircos_regions_departements_circonscriptions_communes_gps.csv')

    coords = extraire_coordonnees(communes)

    features = []
    for e in elevages:
        code_commune = e['EDE'][0:5]

        if code_commune in coords:
            features.append(Feature(geometry=Point(coords[e['EDE'][0:5]]), properties={'title': e['NOM']}))
        else:
            print("Commune manquante: " + code_commune)

    collection = FeatureCollection(features)

    with open('data/elevages.json', 'w') as f:
        dump(collection, f)
