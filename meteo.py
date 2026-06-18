from datetime import datetime, timedelta
import pandas as pd
from meteostat import Daily

try:
    station_id = '71628'
    
    # On définit "aujourd'hui" explicitement en date (sans heure)
    aujourdhui = datetime.now().date()
    
    # On demande une plage large pour être sûr d'avoir assez de jours (14 jours)
    debut = aujourdhui - timedelta(days=14)
    fin = aujourdhui
    
    # Récupération
    data = Daily(station_id, debut, fin)
    data = data.fetch()
    
    # FILTRE CRUCIAL : On ne garde que les lignes dont la date est STRICTEMENT INFÉRIEURE à aujourd'hui
    data = data[data.index.date < aujourdhui]
    
    # On prend les 7 dernières lignes de ce résultat filtré
    data_final = data.tail(7)
    
    # Construction du rapport
    lignes = ["Précipitations totales des sept derniers jours :"]
    
    if not data_final.empty and 'prcp' in data_final.columns:
        for date, row in data_final.iterrows():
            date_str = date.strftime('%d/%m')
            valeur = row['prcp'] if row['prcp'] == row['prcp'] else 0.0
            lignes.append(f"{date_str}: {valeur:.1f} mm")
        
        total_semaine = data_final['prcp'].fillna(0).sum()
        lignes.append(f"Total: {total_semaine:.1f} mm")
    else:
        lignes.append("Données en attente")
        
    resultat = "\n".join(lignes)

except Exception as e:
    resultat = f"Erreur de lecture: {str(e)}"

with open("resultat.txt", "w") as f:
    f.write(resultat)
