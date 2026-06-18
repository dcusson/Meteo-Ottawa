from datetime import datetime, timedelta
from meteostat import Daily

try:
    station_id = '71628'
    fin = datetime.now() - timedelta(days=1)
    debut = datetime.now() - timedelta(days=7)
    
    data = Daily(station_id, debut, fin)
    data = data.fetch()
    
    if not data.empty and 'prcp' in data.columns:
        lignes = []
        # On parcourt chaque jour de l'intervalle
        for date, row in data.iterrows():
            date_str = date.strftime('%d/%m') # Format : 10/06
            valeur = row['prcp'] if row['prcp'] == row['prcp'] else 0.0 # Gestion des NaN
            lignes.append(f"{date_str}: {valeur:.1f} mm")
        
        # On joint tout avec des retours à la ligne
        resultat = "\n".join(lignes)
    else:
        resultat = "Aucune donnée disponible"

except Exception:
    resultat = "Erreur de lecture"

with open("resultat.txt", "w") as f:
    f.write(resultat)
