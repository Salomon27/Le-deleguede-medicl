import sqlite3

# Connexion à la base de données
conn = sqlite3.connect('pharmacy_management.db')
cursor = conn.cursor()

# Création des tables Produits, Visites et Taches
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Produits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        quantité INTEGER NOT NULL,
        prix_unitaire REAL NOT NULL,
        date_expiration DATE
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Visites (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        prescripteur_nom TEXT NOT NULL,
        date_visite DATE NOT NULL,
        compte_rendu TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Taches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        description TEXT NOT NULL,
        date_limite DATE NOT NULL,
        statut TEXT CHECK(statut IN ('En attente', 'En cours', 'Terminé'))
    )
''')

# Sauvegarde des modifications et fermeture de la connexion
conn.commit()
conn.close()

print("Base de données initialisée avec succès.")
