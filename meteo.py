from datetime import datetime, timedelta
from meteostat import Daily

try:
    station_id = '71628'
    
    # Pour avoir 7 jours : fin = hier, debut = hier - 7 jours
    # On utilise 8 jours pour la fenêtre de recherche afin d'être certain d'avoir 7 jours complets
    fin = datetime.now() - timedelta(days=1)
    debut = datetime.now() - timedelta(days=8)
    
    # Récupération des données
    data = Daily(station_id, debut, fin)
    data = data.fetch()
    
    # On force la sélection des 7 dernières lignes disponibles
    data_final = data.tail(7)
    
    # Construction du rapport
    lignes = ["Précipitations totales des sept derniers jours :"]
    
    if not data_final.empty and 'prcp' in data_final.columns:
        for date, row in data_final.iterrows():
            date_str = date.strftime('%d/%m')
            valeur = row['prcp'] if row['prcp'] == row['prcp'] else 0.0
            lignes.append(f"{date_str}: {valeur:.1f} mm")
        
        # Calcul du total
        total_semaine = data_final['prcp'].fillna(0).sum()
        lignes.append(f"Total: {total_semaine:.1f} mm")
    else:
        lignes.append("Données non disponibles")
        
    resultat = "\n".join(lignes)

except Exception as e:
    resultat = f"Erreur de lecture: {str(e)}"

with open("resultat.txt", "w") as f:
    f.write(resultat)
