from datetime import datetime, timedelta
from meteostat import Daily
import pandas as pd

try:
    station_id = '71628'
    
    # 1. On définit "aujourd'hui" comme minuit aujourd'hui (00:00:00)
    aujourdhui_minuit = pd.Timestamp.now().normalize()
    
    # 2. On définit la fin à hier soir (23:59:59) et le début à 7 jours avant
    fin = aujourdhui_minuit - timedelta(seconds=1)
    debut = aujourdhui_minuit - timedelta(days=7)
    
    data = Daily(station_id, debut, fin)
    data = data.fetch()
    
    # 3. Sécurité supplémentaire : on filtre pour être certain de n'avoir que le passé
    data = data[data.index < aujourdhui_minuit]
    
    # On prend les 7 derniers jours disponibles dans ce bloc
    data_final = data.tail(7)
    
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
