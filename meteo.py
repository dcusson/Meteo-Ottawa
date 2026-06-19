from datetime import datetime, timedelta
from meteostat import Daily
import pandas as pd

import sys
print(sys.version)

try:
    station_id = '71628'
    
    # 1. Obtenir l'heure d'Ottawa (UTC-4)
    maintenant_ottawa = datetime.utcnow() - timedelta(hours=4)
    aujourdhui = maintenant_ottawa.date()
    
    # 2. Générer la liste des 8 derniers jours (excluant aujourd'hui)
    # Du plus vieux au plus récent (ex: de J-8 à J-1)
    dates_voulues = [(aujourdhui - timedelta(days=i)) for i in range(8, 0, -1)]
    
    # 3. Paramètres de recherche pour Meteostat
    debut_dt = datetime.combine(dates_voulues[0], datetime.min.time())
    fin_dt = datetime.combine(dates_voulues[-1], datetime.max.time())
    
    data = Daily(station_id, debut_dt, fin_dt)
    data = data.fetch()
    
    # 4. Construction de votre fichier texte
    lignes = ["Précipitations mesurées des huit derniers jours :"]
    
    toutes_les_valeurs = []
    hier_est_publie = False
    
    # On boucle sur nos 8 dates
    for index, d in enumerate(dates_voulues):
        date_str = d.strftime('%d/%m')
        d_timestamp = pd.Timestamp(d)
        valeur_jour = 0.0
        est_publie_ce_jour = False
        
        # Si la date existe dans les données téléchargées
        if not data.empty and d_timestamp in data.index:
            valeur = data.loc[d_timestamp, 'prcp']
            if pd.notna(valeur):
                valeur_jour = float(valeur)
                est_publie_ce_jour = True
            lignes.append(f"{date_str}: {valeur_jour:.1f} mm")
        else:
            lignes.append(f"{date_str}: Donnée en attente (non publiée)")
            
        # On garde en mémoire la valeur (0.0 ou réelle) pour le calcul final
        toutes_les_valeurs.append(valeur_jour)
        
        # Le dernier index (7) correspond à hier. On note s'il est publié ou non.
        if index == 7 and est_publie_ce_jour:
            hier_est_publie = True
            
    # 5. Application de votre règle de calcul pour le total
    if hier_est_publie:
        # Cas 1 : 8 résultats complets -> Somme des 7 plus récents (on ignore le plus vieux à l'index 0)
        total_7_jours = sum(toutes_les_valeurs[1:])
        texte_total = "Total des 7 derniers jours"
    else:
        # Cas 2 : Hier non publié -> Somme des 7 premiers complets (on ignore hier à l'index 7)
        total_7_jours = sum(toutes_les_valeurs[:7])
        texte_total = "Total des 7 derniers jours complets (hier exclu)"
    
    lignes.append("") # Ligne vide pour aérer la lecture
    lignes.append(f"{texte_total}: {total_7_jours:.1f} mm")
    
    resultat = "\n".join(lignes)

except Exception as e:
    resultat = f"Erreur de lecture: {str(e)}"

with open("resultat.txt", "w") as f:
    f.write(resultat)
