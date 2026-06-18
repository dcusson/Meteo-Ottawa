from datetime import datetime, timedelta
from meteostat import Daily
import pandas as pd

try:
    station_id = '71628'
    
    # Calcul manuel des dates (UTC-4 pour Ottawa)
    maintenant = datetime.utcnow() - timedelta(hours=4)
    hier = maintenant.date() - timedelta(days=1)
    debut = hier - timedelta(days=6)
    
    # Récupération
    data = Daily(station_id, debut, hier)
    data = data.fetch()
    
    # CORRECTION : On convertit l'index de pandas en date pour permettre la comparaison
    data = data[data.index.normalize() <= pd.Timestamp(hier)]
    
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
