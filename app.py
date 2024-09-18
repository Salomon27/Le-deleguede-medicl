from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Connexion à la base de données
def get_db_connection():
    conn = sqlite3.connect('pharmacy_management.db')
    conn.row_factory = sqlite3.Row  # Retourner les lignes sous forme de dictionnaire
    return conn

# Route pour la page d'accueil
@app.route('/')
def index():
    return render_template('base.html')

# Routes pour la gestion des produits
@app.route('/produits')
def produits():
    conn = get_db_connection()
    produits = conn.execute('SELECT * FROM Produits').fetchall()
    conn.close()
    return render_template('produits.html', produits=produits)

@app.route('/ajouter_produit', methods=('GET', 'POST'))
def ajouter_produit():
    if request.method == 'POST':
        nom = request.form['nom']
        quantite = request.form['quantite']
        prix = request.form['prix']
        expiration = request.form['expiration']

        conn = get_db_connection()
        conn.execute('INSERT INTO Produits (nom, quantité, prix_unitaire, date_expiration) VALUES (?, ?, ?, ?)',
                     (nom, quantite, prix, expiration))
        conn.commit()
        conn.close()

        return redirect(url_for('produits'))
    return render_template('ajouter_produit.html')

@app.route('/modifier_produit/<int:id>', methods=('GET', 'POST'))
def modifier_produit(id):
    conn = get_db_connection()
    produit = conn.execute('SELECT * FROM Produits WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        nom = request.form['nom']
        quantite = request.form['quantite']
        prix = request.form['prix']
        expiration = request.form['expiration']

        conn.execute('UPDATE Produits SET nom = ?, quantité = ?, prix_unitaire = ?, date_expiration = ? WHERE id = ?',
                     (nom, quantite, prix, expiration, id))
        conn.commit()
        conn.close()

        return redirect(url_for('produits'))

    conn.close()
    return render_template('modifier_produit.html', produit=produit)

@app.route('/supprimer_produit/<int:id>', methods=('POST',))
def supprimer_produit(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM Produits WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('produits'))

# Routes pour la gestion des visites
@app.route('/visites')
def visites():
    conn = get_db_connection()
    visites = conn.execute('SELECT * FROM Visites').fetchall()
    conn.close()
    return render_template('visites.html', visites=visites)

@app.route('/ajouter_visite', methods=('GET', 'POST'))
def ajouter_visite():
    if request.method == 'POST':
        prescripteur = request.form['prescripteur']
        date_visite = request.form['date_visite']
        compte_rendu = request.form['compte_rendu']

        conn = get_db_connection()
        conn.execute('INSERT INTO Visites (prescripteur_nom, date_visite, compte_rendu) VALUES (?, ?, ?)',
                     (prescripteur, date_visite, compte_rendu))
        conn.commit()
        conn.close()

        return redirect(url_for('visites'))
    return render_template('ajouter_visite.html')

@app.route('/modifier_visite/<int:id>', methods=('GET', 'POST'))
def modifier_visite(id):
    conn = get_db_connection()
    visite = conn.execute('SELECT * FROM Visites WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        prescripteur = request.form['prescripteur']
        date_visite = request.form['date_visite']
        compte_rendu = request.form['compte_rendu']

        conn.execute('UPDATE Visites SET prescripteur_nom = ?, date_visite = ?, compte_rendu = ? WHERE id = ?',
                     (prescripteur, date_visite, compte_rendu, id))
        conn.commit()
        conn.close()

        return redirect(url_for('visites'))

    conn.close()
    return render_template('modifier_visite.html', visite=visite)

@app.route('/supprimer_visite/<int:id>', methods=('POST',))
def supprimer_visite(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM Visites WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('visites'))

# Routes pour la gestion des tâches
@app.route('/taches')
def taches():
    conn = get_db_connection()
    taches = conn.execute('SELECT * FROM Taches').fetchall()
    conn.close()
    return render_template('taches.html', taches=taches)

@app.route('/ajouter_tache', methods=('GET', 'POST'))
def ajouter_tache():
    if request.method == 'POST':
        description = request.form['description']
        date_limite = request.form['date_limite']
        statut = request.form['statut']

        conn = get_db_connection()
        conn.execute('INSERT INTO Taches (description, date_limite, statut) VALUES (?, ?, ?)',
                     (description, date_limite, statut))
        conn.commit()
        conn.close()

        return redirect(url_for('taches'))
    return render_template('ajouter_tache.html')

@app.route('/modifier_tache/<int:id>', methods=('GET', 'POST'))
def modifier_tache(id):
    conn = get_db_connection()
    tache = conn.execute('SELECT * FROM Taches WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        description = request.form['description']
        date_limite = request.form['date_limite']
        statut = request.form['statut']

        conn.execute('UPDATE Taches SET description = ?, date_limite = ?, statut = ? WHERE id = ?',
                     (description, date_limite, statut, id))
        conn.commit()
        conn.close()

        return redirect(url_for('taches'))

    conn.close()
    return render_template('modifier_tache.html', tache=tache)

@app.route('/supprimer_tache/<int:id>', methods=('POST',))
def supprimer_tache(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM Taches WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('taches'))

# Route pour la visualisation des données
@app.route('/visualiser_donnees')
def visualiser_donnees():
    conn = get_db_connection()
    produits = conn.execute('SELECT * FROM Produits').fetchall()
    visites = conn.execute('SELECT * FROM Visites').fetchall()
    taches = conn.execute('SELECT * FROM Taches').fetchall()
    conn.close()
    return render_template('visualiser_donnees.html', produits=produits, visites=visites, taches=taches)

# Route pour modifier les données génériques
@app.route('/modifier_donnees/<table>/<int:id>', methods=('GET', 'POST'))
def modifier_donnees(table, id):
    conn = get_db_connection()
    item = None

    if table == 'Produits':
        item = conn.execute('SELECT * FROM Produits WHERE id = ?', (id,)).fetchone()
        if request.method == 'POST':
            nom = request.form['nom']
            quantite = request.form['quantite']
            prix = request.form['prix']
            expiration = request.form['expiration']
            conn.execute('UPDATE Produits SET nom = ?, quantité = ?, prix_unitaire = ?, date_expiration = ? WHERE id = ?',
                         (nom, quantite, prix, expiration, id))
            conn.commit()
    
    elif table == 'Visites':
        item = conn.execute('SELECT * FROM Visites WHERE id = ?', (id,)).fetchone()
        if request.method == 'POST':
            prescripteur = request.form['prescripteur']
            date_visite = request.form['date_visite']
            compte_rendu = request.form['compte_rendu']
            conn.execute('UPDATE Visites SET prescripteur_nom = ?, date_visite = ?, compte_rendu = ? WHERE id = ?',
                         (prescripteur, date_visite, compte_rendu, id))
            conn.commit()
    
    elif table == 'Taches':
        item = conn.execute('SELECT * FROM Taches WHERE id = ?', (id,)).fetchone()
        if request.method == 'POST':
            description = request.form['description']
            date_limite = request.form['date_limite']
            statut = request.form['statut']
            conn.execute('UPDATE Taches SET description = ?, date_limite = ?, statut = ? WHERE id = ?',
                         (description, date_limite, statut, id))
            conn.commit()

    conn.close()
    return render_template(f'modifier_{table.lower()}.html', item=item)

# Route pour supprimer des données génériques
@app.route('/supprimer_donnees/<table>/<int:id>', methods=('POST',))
def supprimer_donnees(table, id):
    conn = get_db_connection()
    if table == 'Produits':
        conn.execute('DELETE FROM Produits WHERE id = ?', (id,))
    elif table == 'Visites':
        conn.execute('DELETE FROM Visites WHERE id = ?', (id,))
    elif table == 'Taches':
        conn.execute('DELETE FROM Taches WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('visualiser_donnees'))

# Route pour visualiser les produits
@app.route('/visualiser_produits')
def visualiser_produits():
    conn = get_db_connection()
    produits = conn.execute('SELECT * FROM Produits').fetchall()
    conn.close()
    return render_template('visualiser_produits.html', produits=produits)

# Route pour visualiser les visites
@app.route('/visualiser_visites')
def visualiser_visites():
    conn = get_db_connection()
    visites = conn.execute('SELECT * FROM Visites').fetchall()
    conn.close()
    return render_template('visualiser_visites.html', visites=visites)

# Route pour visualiser les tâches
@app.route('/visualiser_taches')
def visualiser_taches():
    conn = get_db_connection()
    taches = conn.execute('SELECT * FROM Taches').fetchall()
    conn.close()
    return render_template('visualiser_taches.html', taches=taches)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)