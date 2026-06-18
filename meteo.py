from datetime import datetime, timedelta
from meteostat import Daily

try:
    # ID de la station de l'aéroport international d'Ottawa
    station_id = '71628'
    
    # On définit une plage large (10 jours) pour s'assurer d'avoir assez de données
    fin = datetime.now() - timedelta(days=1)
    debut = datetime.now() - timedelta(days=10)
    
    # Récupération des données
    data = Daily(station_id, debut, fin)
    data = data.fetch()
    
    # On garde uniquement les 7 dernières lignes disponibles pour être certain d'avoir 7 jours
    if not data.empty and 'prcp' in data.columns:
        data_final = data.tail(7)
        
        lignes = []
        # On parcourt ces 7 jours pour construire le rapport
        for date, row in data_final.iterrows():
            date_str = date.strftime('%d/%m')
            # Gestion sécurisée des valeurs manquantes (NaN)
            valeur = row['prcp'] if row['prcp'] == row['prcp'] else 0.0
            lignes.append(f"{date_str}: {valeur:.1f} mm")
        
        # On ajoute le total à la fin du fichier pour votre information
        total_semaine = data_final['prcp'].fillna(0).sum()
        lignes.append(f"Total: {total_semaine:.1f} mm")
        
        resultat = "\n".join(lignes)
    else:
        resultat = "Aucune donnée disponible"

except Exception:
    resultat = "Erreur lors de la récupération"

# Écriture dans le fichier
with open("resultat.txt", "w") as f:
    f.write(resultat)
