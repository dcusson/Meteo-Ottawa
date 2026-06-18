from datetime import datetime, timedelta
from meteostat import Daily
import pandas as pd

try:
    station_id = '71628'
    
    # Calcul des dates en format texte YYYY-MM-DD pour éviter les conflits de types
    maintenant = datetime.utcnow() - timedelta(hours=4)
    hier_date = maintenant.date() - timedelta(days=1)
    debut_date = hier_date - timedelta(days=6)
    
    # Récupération des données
    data = Daily(station_id, debut_date, hier_date)
    data = data.fetch()
    
    # CORRECTION TOTALE : On convertit l'index en format texte (string) pour comparer
    # Cela annule tous les problèmes de types entre datetime et pandas
    data = data[data.index.strftime('%Y-%m-%d') <= str(hier_date)]
    
    if not data.empty and 'prcp' in data.columns:
        lignes = ["Précipitations totales des 7 derniers jours :"]
        for date, row in data.iterrows():
            date_str = date.strftime('%d/%m')
            valeur = row['prcp'] if row['prcp'] == row['prcp'] else 0.0
            lignes.append(f"{date_str}: {valeur:.1f} mm")
        
        total_semaine = data['prcp'].fillna(0).sum()
        lignes.append(f"Total: {total_semaine:.1f} mm")
        resultat = "\n".join(lignes)
    else:
        resultat = "Données en attente"

except Exception as e:
    resultat = f"Erreur de lecture: {str(e)}"

with open("resultat.txt", "w") as f:
    f.write(resultat)
