from datetime import datetime, timedelta
from meteostat import Daily
import pandas as pd

try:
    station_id = '71628'
    
    # 1. Obtenir l'heure d'Ottawa (UTC-4) de façon fiable
    maintenant_ottawa = datetime.utcnow() - timedelta(hours=4)
    aujourdhui = maintenant_ottawa.date()
    
    # 2. Générer la liste EXACTE des 8 derniers jours (du plus vieux au plus récent)
    # Si aujourd'hui = 19 juin, cela génère du 11 au 18 juin.
    dates_voulues = [(aujourdhui - timedelta(days=i)) for i in range(8, 0, -1)]
    
    # 3. Paramètres de recherche pour Meteostat
    debut_dt = datetime.combine(dates_voulues[0], datetime.min.time())
    fin_dt = datetime.combine(dates_voulues[-1], datetime.max.time())
    
    data = Daily(station_id, debut_dt, fin_dt)
    data = data.fetch()
    
    # 4. Construction de votre fichier texte
    lignes = ["Précipitations mesurées des 8 derniers jours :"]
    total_semaine = 0.0
    
    # On boucle strictement sur nos 8 dates, une par une
    for d in dates_voulues:
        date_str = d.strftime('%d/%m')
        d_timestamp = pd.Timestamp(d)
        
        # Si la date existe dans les données téléchargées
        if not data.empty and d_timestamp in data.index:
            valeur = data.loc[d_timestamp, 'prcp']
            # Gérer le cas où la donnée existe mais est "NaN" (vide)
            if pd.isna(valeur):
                valeur = 0.0
            lignes.append(f"{date_str}: {valeur:.1f} mm")
            total_semaine += valeur
        else:
            # Si Meteostat n'a pas encore publié cette date
            lignes.append(f"{date_str}: Donnée en attente (non publiée)")
            
    lignes.append(f"Total: {total_semaine:.1f} mm")
    resultat = "\n".join(lignes)

except Exception as e:
    resultat = f"Erreur de lecture: {str(e)}"

with open("resultat.txt", "w") as f:
    f.write(resultat)
