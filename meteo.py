from datetime import datetime, timedelta
from meteostat import Daily, Point
import os

try:
    # Coordonnées pour Ottawa
    lat, lon = 45.4215, -75.6972
    
    # Période : hier
    hier = datetime.now() - timedelta(days=1)
    debut = datetime(hier.year, hier.month, hier.day)
    
    # Récupération des données
    emplacement = Point(lat, lon)
    donnees = Daily(emplacement, debut, debut)
    donnees = donnees.fetch()
    
    if not donnees.empty and 'prcp' in donnees.columns:
        pluie = donnees['prcp'].iloc[0]
        resultat = str(pluie)
    else:
        resultat = "0.0"
except Exception:
    resultat = "0.0"

# Écriture du résultat dans un fichier texte
with open("resultat.txt", "w") as f:
    f.write(resultat)
