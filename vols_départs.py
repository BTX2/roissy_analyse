from bs4 import BeautifulSoup
import requests
from geopy.geocoders import Nominatim
import folium
import warnings

url = "https://www.aeroports-paris.info/index.php?page=departs&airport=roissy"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

liste_départ = soup.find_all("a", {"class": "airport-link"})

liste_localisation_x = []
liste_localisation_y = []

x_roissy = 2.547925
y_roissy = 49.009691

geolocator = Nominatim(user_agent="thibault_marchal@yahoo.fr")
maps = folium.Map(location=[y_roissy, x_roissy], zoom_start=5)

for i in range(0, len(liste_départ)):
    try:
        localisation = geolocator.geocode(liste_départ[i].text)
        liste_localisation_x.append(localisation.longitude)
        liste_localisation_y.append(localisation.latitude)
        print("[...] {} : OK".format(liste_départ[i].text))
    except:
        print("ERREUR : {} : ne trouve pas".format(liste_départ[i].text))


for i in range(0, len(liste_localisation_x)):
    folium.Marker([liste_localisation_y[i],
                  liste_localisation_x[i]]).add_to(maps)

maps.save("maps_ville_arrivé.html")
