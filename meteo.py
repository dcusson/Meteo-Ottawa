from datetime import datetime, timedelta
from meteostat import Daily

try:
    station_id = '71628'
    
    # On définit la période pour inclure exactement les 7 jours avant aujourd'hui
    fin = datetime.now() - timedelta(days=1)
    debut = datetime.now() - timedelta(days=8)
    
    data = Daily(station_id, debut, fin)
    data = data.fetch()
    
    # On prend les 7 premiers jours de la série (du plus vieux au plus récent)
    data_final = data.head(7)
    
    lignes = ["Précipitations totales des 7 derniers jours :"]
    
    if not data_final.empty and 'prcp' in data_final.columns:
        for date, row in data_final.iterrows():
            date_str = date.strftime('%d/%m')
            valeur = row['prcp'] if row['prcp'] == row['prcp'] else 0.0
            lignes.append(f"{date_str}: {valeur:.1f} mm")
        
        total_semaine = data_final['prcp'].fillna(0).sum()
        lignes.append(f"Total: {total_semaine:.1f} mm")
    else:
        lignes.append("Données non disponibles")
        
    resultat = "\n".join(lignes)

except Exception as e:
    resultat = f"Erreur de lecture: {str(e)}"

with open("resultat.txt", "w") as f:
    f.write(resultat)
