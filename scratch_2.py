import serial
import csv
from datetime import datetime, timedelta

# Configuration du port COM
port = serial.Serial('COM3', baudrate=9600, timeout=1)

# Variables pour suivre le début et la fin de l'intervalle de 5 minutes
interval_start = datetime.now()
interval_end = interval_start + timedelta(minutes=5)

# Fonction pour traiter les données
def traiter_donnees(data):
    # Supposons que les données reçues sont sous la forme d'un nombre entier (en milliwatts)
    quantite_consommee_mw = int(data)
    # Calculer le prix en multipliant la quantité consommée (en mW) par le prix par kilowattheure (185)
    prix = quantite_consommee_mw * (185 )  # Convertir de milliwatts à kilowatts
    # Ajouter un timestamp actuel
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return timestamp, quantite_consommee_mw, prix

# Ouvrir un fichier CSV pour écrire les données
with open('donnees.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    # Écrire l'en-tête du fichier CSV
    writer.writerow(['Timestamp', 'Quantité consommée (mW)', 'Prix'])

    # Lecture et traitement des données en continu
    while True:
        # Lecture des données du port COM
        data = port.readline().decode('ascii', errors='ignore').strip()

        # Vérifier si l'intervalle de 5 minutes est terminé
        if datetime.now() >= interval_end:
            # Réinitialiser les variables de début et fin d'intervalle
            interval_start = datetime.now()
            interval_end = interval_start + timedelta(minutes=5)
            # Effacer le fichier CSV
            file.truncate(0)
            file.seek(0)
            # Réécrire l'en-tête du fichier CSV
            writer.writerow(['Timestamp', 'Quantité consommée (mW)', 'Prix'])

        # Traitement des données
        timestamp, quantite_consommee, prix = traiter_donnees(data)

        # Écrire les données dans le fichier CSV
        writer.writerow([timestamp, quantite_consommee, int(prix)])
