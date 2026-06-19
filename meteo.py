from datetime import datetime, timedelta
from meteostat import Daily
import pandas as pd

try:
    station_id = '71628'
    
    # 1. Obtenir l'heure d'Ottawa (UTC-4) de façon fiable
    maintenant_ottawa = datetime.utcnow() - timedelta(hours=4)
    aujourdhui = maintenant_ottawa.date()
    
    # 2. Générer la liste EXACTE des 8 derniers jours (excluant aujourd'hui)
    # Du plus vieux au plus récent (ex: du J-8 jusqu'à hier)
    dates_voulues = [(aujourdhui - timedelta(days=i)) for i in range(8, 0, -1)]
    
    # 3. Paramètres de recherche pour Meteostat
    debut_dt = datetime.combine(dates_voulues[0], datetime.min.time())
    fin_dt = datetime.combine(dates_voulues[-1], datetime.max.time())
    
    data = Daily(station_id, debut_dt, fin_dt)
    data = data.fetch()
    
    # 4. Construction de votre fichier texte
    lignes = ["Précipitations mesurées des huit derniers jours :"]
    
    valeurs_8_jours = []
    valeurs_7_derniers = []
    
    # On boucle sur nos 8 dates
    for index, d in enumerate(dates_voulues):
        date_str = d.strftime('%d/%m')
        d_timestamp = pd.Timestamp(d)
        valeur_jour = 0.0
        
        # Si la date existe dans les données téléchargées
        if not data.empty and d_timestamp in data.index:
            valeur = data.loc[d_timestamp, 'prcp']
            # Si la valeur n'est pas vide (NaN)
            if pd.notna(valeur):
                valeur_jour = float(valeur)
            lignes.append(f"{date_str}: {valeur_jour:.1f} mm")
        else:
            lignes.append(f"{date_str}: Donnée en attente (non publiée)")
            # valeur_jour reste à 0.0 pour ne pas fausser les totaux
            
        # On ajoute la valeur au total des 8 jours
        valeurs_8_jours.append(valeur_jour)
        
        # Le premier jour de la boucle (index 0) est le jour 8 (le plus ancien).
        # Pour le total des 7 *derniers* jours (les plus récents), on l'ignore.
        if index > 0:
            valeurs_7_derniers.append(valeur_jour)
            
    # 5. Calcul et ajout des deux totaux
    total_7_jours = sum(valeurs_7_derniers)
    total_8_jours = sum(valeurs_8_jours)
    
    # J'ai ajouté une ligne vide pour espacer les résultats des totaux
    lignes.append("") 
    lignes.append(f"Total des 7 derniers jours: {total_7_jours:.1f} mm")
    lignes.append(f"Total des 8 derniers jours: {total_8_jours:.1f} mm")
    
    resultat = "\n".join(lignes)

except Exception as e:
    resultat = f"Erreur de lecture: {str(e)}"

with open("resultat.txt", "w") as f:
    f.write(resultat)
