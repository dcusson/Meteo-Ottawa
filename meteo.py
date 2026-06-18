from datetime import datetime, timedelta
import pytz
from meteostat import Daily

try:
    station_id = '71628'
    # Utiliser le fuseau horaire d'Ottawa pour être précis
    tz = pytz.timezone('America/Toronto')
    hier = datetime.now(tz).date() - timedelta(days=1)
    debut = hier - timedelta(days=6) # Pour avoir un bloc de 7 jours (hier compris)
    
    data = Daily(station_id, debut, hier)
    data = data.fetch()
    
    # On s'assure qu'on ne traite que les données jusqu'à hier inclus
    data = data[data.index.date <= hier]
    
    if not data.empty and 'prcp' in data.columns:
        lignes = []
        for date, row in data.iterrows():
            date_str = date.strftime('%d/%m')
            valeur = row['prcp'] if row['prcp'] == row['prcp'] else 0.0
            lignes.append(f"{date_str}: {valeur:.1f} mm")
        
        total_semaine = data['prcp'].fillna(0).sum()
        lignes.append(f"Total: {total_semaine:.1f} mm")
        resultat = "\n".join(lignes)
    else:
        resultat = "Données en attente"

except Exception:
    resultat = "Erreur de lecture"

with open("resultat.txt", "w") as f:
    f.write(resultat)
