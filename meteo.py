from datetime import datetime, timedelta
import pytz
from meteostat import Daily

try:
    station_id = '71628'
    # Utilisation du fuseau horaire d'Ottawa
    tz = pytz.timezone('America/Toronto')
    hier = datetime.now(tz).date() - timedelta(days=1)
    debut = hier - timedelta(days=6)
    
    data = Daily(station_id, debut, hier)
    data = data.fetch()
    
    # Filtrage strict
    data = data[data.index.date <= hier]
    
    if not data.empty and 'prcp' in data.columns:
        # Ajout du titre personnalisé comme première ligne
        lignes = ["Précipitations totales des 7 derniers jours :"]
        
        for date, row in data.iterrows():
            date_str = date.strftime('%d/%m')
            valeur = row['prcp'] if row['prcp'] == row['prcp'] else 0.0
            lignes.append(f"{date_str}: {valeur:.1f} mm")
        
        total_semaine = data['prcp'].fillna(0).sum()
        lignes.append(f"Total: {total_semaine:.1f} mm")
        
        resultat = "\n".join(lignes)
    else:
        resultat = "Précipitations totales des 7 derniers jours :\nDonnées en attente"

except Exception:
    resultat = "Erreur de lecture"

# Écriture dans le fichier
with open("resultat.txt", "w") as f:
    f.write(resultat)
