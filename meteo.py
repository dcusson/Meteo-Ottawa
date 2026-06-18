from datetime import datetime, timedelta
from meteostat import Daily

try:
    station_id = '71628'
    # On demande une période assez longue pour être sûr de couvrir 7 jours complets passés
    fin = datetime.now()
    debut = datetime.now() - timedelta(days=15)
    
    data = Daily(station_id, debut, fin)
    data = data.fetch()
    
    # Filtrage strict : on ne garde que les jours strictement antérieurs à aujourd'hui
    aujourd_hui = datetime.now().date()
    data = data[data.index.date < aujourd_hui]
    
    # On garde les 7 derniers jours de la liste filtrée
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
