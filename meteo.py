from datetime import datetime, timedelta
from meteostat import Daily

try:
    station_id = '71628'
    # On cherche sur une période large pour être sûr d'avoir assez de jours
    fin = datetime.now() - timedelta(days=1)
    debut = datetime.now() - timedelta(days=15)
    
    data = Daily(station_id, debut, fin)
    data = data.fetch()
    
    # Exclure explicitement aujourd'hui
    aujourd_hui = datetime.now().date()
    data = data[data.index.date < aujourd_hui]
    
    # Prendre les 7 derniers jours disponibles
    data_final = data.tail(7)
    
    if not data_final.empty and 'prcp' in data_final.columns:
        lignes = []
        for date, row in data_final.iterrows():
            date_str = date.strftime('%d/%m')
            valeur = row['prcp'] if row['prcp'] == row['prcp'] else 0.0
            lignes.append(f"{date_str}: {valeur:.1f} mm")
        
        total_semaine = data_final['prcp'].fillna(0).sum()
        lignes.append(f"Total: {total_semaine:.1f} mm")
        resultat = "\n".join(lignes)
    else:
        resultat = "Données en cours de traitement"

except Exception:
    resultat = "Erreur de lecture"

with open("resultat.txt", "w") as f:
    f.write(resultat)
