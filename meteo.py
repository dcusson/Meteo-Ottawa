from datetime import datetime
from meteostat import Daily
import pandas as pd

try:
    station_id = '71628'
    aujourdhui = datetime.now().date()
    # On demande une période assez large
    debut = aujourdhui - timedelta(days=15)
    fin = aujourdhui
    
    data = Daily(station_id, debut, fin)
    data = data.fetch()
    
    # Vérification : on affiche les dates trouvées pour diagnostiquer
    dates_disponibles = [d.strftime('%d/%m') for d in data.index]
    
    # Filtrage manuel
    data_filtree = data[data.index.date < aujourdhui]
    data_final = data_filtree.tail(7)
    
    if data_final.empty:
        resultat = f"DEBUG: Dates trouvées dans Meteostat: {dates_disponibles}. Aujourd'hui est {aujourdhui}"
    else:
        lignes = ["Précipitations totales des 7 derniers jours :"]
        for date, row in data_final.iterrows():
            date_str = date.strftime('%d/%m')
            valeur = row['prcp'] if pd.notna(row['prcp']) else 0.0
            lignes.append(f"{date_str}: {valeur:.1f} mm")
        
        total = data_final['prcp'].fillna(0).sum()
        lignes.append(f"Total: {total:.1f} mm")
        resultat = "\n".join(lignes)

except Exception as e:
    resultat = f"Erreur critique: {str(e)}"

with open("resultat.txt", "w") as f:
    f.write(resultat)
