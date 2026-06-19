from datetime import datetime, timedelta
from meteostat import Daily

try:
    station_id = '71628'
    
    # 1. On prend la date d'aujourd'hui (ex: 19 juin) et on la fixe à minuit pile (00:00:00)
    aujourdhui = datetime.utcnow().date()
    aujourdhui_dt = datetime(aujourdhui.year, aujourdhui.month, aujourdhui.day)
    
    # 2. La fin est hier soir à 23h59:59 (aujourd'hui minuit - 1 seconde)
    fin_dt = aujourdhui_dt - timedelta(seconds=1)
    
    # 3. Le début est 7 jours avant aujourd'hui à minuit (ex: 12 juin à 00:00:00)
    debut_dt = aujourdhui_dt - timedelta(days=7)
    
    # Récupération de la période exacte (du 12 à 00h00 jusqu'au 18 à 23h59)
    data = Daily(station_id, debut_dt, fin_dt)
    data = data.fetch()
    
    # Construction de votre fichier texte
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
