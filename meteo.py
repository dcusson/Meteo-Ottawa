from datetime import datetime, timedelta
from meteostat import Daily

try:
    station_id = '71628'
    
    # 1. On calcule les dates "pures" (le jour actuel, sans se soucier de l'heure)
    aujourdhui = datetime.utcnow().date()
    
    # 2. On recule d'un jour pour "fin", et de 6 jours de plus pour "début" (total = 7 jours)
    fin_date = aujourdhui - timedelta(days=1)
    debut_date = fin_date - timedelta(days=6)
    
    # 3. On convertit au format précis attendu par Meteostat (à minuit pile)
    debut_dt = datetime(debut_date.year, debut_date.month, debut_date.day)
    fin_dt = datetime(fin_date.year, fin_date.month, fin_date.day)
    
    # 4. Récupération directe, sans aucun filtrage compliqué
    data = Daily(station_id, debut_dt, fin_dt)
    data = data.fetch()
    
    # 5. Construction de votre fichier texte
    lignes = ["Précipitations mesurées des sept derniers jours :"]
    
    if not data.empty and 'prcp' in data.columns:
        for date, row in data.iterrows():
            date_str = date.strftime('%d/%m')
            valeur = row['prcp'] if row['prcp'] == row['prcp'] else 0.0
            lignes.append(f"{date_str}: {valeur:.1f} mm")
        
        total_semaine = data['prcp'].fillna(0).sum()
        lignes.append(f"Total: {total_semaine:.1f} mm")
    else:
        lignes.append("Données non disponibles")
        
    resultat = "\n".join(lignes)

except Exception as e:
    resultat = f"Erreur de lecture: {str(e)}"

with open("resultat.txt", "w") as f:
    f.write(resultat)
