from datetime import datetime, timedelta
from meteostat import Daily, Point

try:
    # Coordonnées pour Ottawa
    lat, lon = 45.4215, -75.6972
    
    # Définition de la période : les 7 derniers jours (excluant aujourd'hui)
    aujourd_hui = datetime.now()
    fin = aujourd_hui - timedelta(days=1)
    debut = aujourd_hui - timedelta(days=7)
    
    # Récupération des données historiques
    emplacement = Point(lat, lon)
    donnees = Daily(emplacement, debut, fin)
    donnees = donnees.fetch()
    
    if not donnees.empty and 'prcp' in donnees.columns:
        # On additionne toutes les précipitations de la semaine
        pluie_totale = donnees['prcp'].sum()
        # On formate le résultat pour avoir une décimale
        resultat = f"{pluie_totale:.1f}"
    else:
        resultat = "0.0"
except Exception:
    resultat = "0.0"

# Écriture du résultat final dans le fichier texte
with open("resultat.txt", "w") as f:
    f.write(resultat)
