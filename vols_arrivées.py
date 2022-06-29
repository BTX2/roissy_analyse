from bs4 import BeautifulSoup
import requests
from geopy.geocoders import Nominatim
import folium
import warnings
import numpy as np
import time


def process_recup(compteur):

    # récuperation des noms des villes

    url = "https://www.aeroports-paris.info/index.php?page=arrivees&airport=roissy"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    liste_arrivées = soup.find_all("a", {"class": "airport-link"})
    liste_vols = soup.find_all("td", {"class": "t-flight"})

    # reformuler les matricules des avions

    for i in range(0, len(liste_vols)):
        liste_vols[i] = liste_vols[i].text
        liste_vols[i] = liste_vols[i].replace(" ", "")

    # création de la map et configuration de la localisation

    x_roissy = 2.547925
    y_roissy = 49.009691

    geolocator = Nominatim(user_agent="thibault_marchal@yahoo.fr")
    maps = folium.Map(location=[y_roissy, x_roissy], zoom_start=5)

    # création des listes avec les coordonnées : la liste des villes départs a les coordonnées

    liste_villes_départs = []
    liste_localisation_x = []
    liste_localisation_y = []
    liste_vols_final = []

    # remplir les listes du dessus
    compteur = 0
    for i in range(0, len(liste_arrivées)):
        try:
            localisation = geolocator.geocode(liste_arrivées[i].text)
            liste_villes_départs.append(
                [liste_arrivées[i].text, localisation.longitude, localisation.latitude])
            liste_localisation_x.append(localisation.longitude)
            liste_localisation_y.append(localisation.latitude)
            liste_vols_final.append(liste_vols[i])
            print("[...] {} : OK".format(liste_arrivées[i].text))
            compteur += 1
        except:
            print("ERREUR : {} : ne trouve pas".format(liste_arrivées[i].text))
            pass
    stat_liste = round((compteur/len(liste_arrivées))*100, 2)
    print("il y a {} %  des villes qui sont sur la map".format(stat_liste))
    print("il y a {} villes de départs".format(compteur))

    # création des marqueurs sur la map

    for i in range(0, len(liste_localisation_x)):
        folium.Marker([liste_localisation_y[i],
                      liste_localisation_x[i]], popup=liste_vols_final[i]).add_to(maps)
    folium.Marker(location=[y_roissy, x_roissy],
                  popup="CDG").add_to(maps)

    # sauver le fichier de la map

    maps.save("maps_villes_départs.html")

    # sauver les données dans un fichier csv

    nom_fichier = "save_liste_" + str(compteur) + ".csv"
    warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning)
    np.savetxt(nom_fichier, liste_arrivées, delimiter=",", fmt='% s')


compteur = 0
while True:
    compteur += 1
    process_recup(compteur)
    time.sleep(3600)
