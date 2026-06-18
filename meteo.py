from datetime import datetime, timedelta
from meteostat import Daily

try:
    # ID de la station de l'aéroport international d'Ottawa
    station_id = '71628'
    
    # Définition de la période : les 7 derniers jours (du plus ancien au plus récent)
    # On prend une marge pour s'assurer d'avoir les 7 jours complets
    fin = datetime.now() - timedelta(days=1)
    debut = datetime.now() - timedelta(days=8)
    
    # Récupération des données historiques
    data = Daily(station_id, debut, fin)
    data = data.fetch()
    
    # Vérification si des données existent
    if not data.empty and 'prcp' in data.columns:
        # On remplace les valeurs manquantes (NaN) par 0, puis on fait la somme
        pluie_totale = data['prcp'].fillna(0).sum()
        
        # On formate le résultat : une seule décimale
        resultat = f"{pluie_totale:.1f}"
    else:
        # Si aucune donnée n'est disponible pour la station
        resultat = "0.0"

except Exception as e:
    # En cas d'erreur de connexion ou autre, on inscrit 0.0
    resultat = "0.0"

# Écriture du résultat final dans le fichier texte pour votre Raccourci
with open("resultat.txt", "w") as f:
    f.write(resultat)
