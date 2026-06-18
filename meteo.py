from datetime import datetime, timedelta
from meteostat import Daily

try:
    station_id = '71628'
    
    # On définit les dates simplement
    # 'fin' est hier, 'debut' est 6 jours avant hier (donc 7 jours au total)
    fin = datetime.now() - timedelta(days=1)
    debut = datetime.now() - timedelta(days=7)
    
    # Récupération directe des 7 jours
    data = Daily(station_id, debut, fin)
    data = data.fetch()
    
    # Construction du rapport
    lignes = ["Précipitations totales des 7 derniers jours :"]
    
    if not data.empty and 'prcp' in data.columns:
        for date, row in data.iterrows():
            date_str = date.strftime('%d/%m')
            valeur = row['prcp'] if row['prcp'] == row['prcp'] else 0.0
            lignes.append(f"{date_str}: {valeur:.1f} mm")
        
        # Calcul du total
        total_semaine = data['prcp'].fillna(0).sum()
        lignes.append(f"Total: {total_semaine:.1f} mm")
    else:
        lignes.append("Données non disponibles")
        
    resultat = "\n".join(lignes)

except Exception as e:
    resultat = f"Erreur de lecture: {str(e)}"

with open("resultat.txt", "w") as f:
    f.write(resultat)
