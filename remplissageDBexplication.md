DERNIER script est plutot adapté au projet à voir
Pour remplir la base de données MariaDB avec ton code Python, tu peux utiliser une bibliothèque comme **`mysql-connector-python`** ou **`pymysql`** pour interagir avec MariaDB. Ces bibliothèques permettent de se connecter à la base de données, d'insérer des données dans les tables, et d'exécuter des requêtes SQL.

---

### **Étape 1 : Installer la bibliothèque Python**
Pour interagir avec MariaDB, installe la bibliothèque `mysql-connector-python` (ou `pymysql` si tu préfères).

```bash
pip install mysql-connector-python
```

---

### **Étape 2 : Script Python pour insérer des données**

Voici un exemple de script Python qui insère des données dans la table `capteurs` de la base de données `iot_project`.

#### Exemple de script Python
```python
import mysql.connector
from datetime import datetime

# Configuration de la connexion à la base de données
db_config = {
    'host': 'localhost',         # Adresse du serveur MariaDB
    'user': 'iot_user',          # Nom de l'utilisateur MariaDB
    'password': 'secure_password',  # Mot de passe de l'utilisateur
    'database': 'iot_project'    # Nom de la base de données
}

# Connexion à la base de données
try:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    print("Connexion à la base de données réussie.")
except mysql.connector.Error as err:
    print(f"Erreur de connexion : {err}")
    exit()

# Fonction pour insérer des données dans la table capteurs
def insert_sensor_data(nom, adresse_mac, temperature, humidite, batterie):
    try:
        # Requête SQL pour insérer des données
        query = """
        INSERT INTO capteurs (nom, adresse_mac, temperature, humidite, batterie, horodatage)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        # Valeurs à insérer
        values = (nom, adresse_mac, temperature, humidite, batterie, datetime.now())

        # Exécuter la requête
        cursor.execute(query, values)
        conn.commit()  # Valider les changements
        print(f"Données insérées : {values}")
    except mysql.connector.Error as err:
        print(f"Erreur lors de l'insertion : {err}")

# Exemple d'insertion de données
insert_sensor_data("Capteur1", "D6:1C:BF:B7:76:62", 22.5, 60.0, 80)
insert_sensor_data("Capteur2", "D7:EF:13:27:15:29", 25.0, 55.0, 75)
insert_sensor_data("Capteur3", "D6:C6:C7:39:A2:E8", 20.0, 65.0, 90)

# Fermer la connexion
cursor.close()
conn.close()
print("Connexion à la base de données fermée.")
```

---

### **Explications du script**

1. **Connexion à la base de données** :
   - La connexion est établie avec `mysql.connector.connect()` en utilisant les paramètres de connexion (`host`, `user`, `password`, `database`).
   - Si la connexion échoue, une exception est levée et affichée.

2. **Insertion des données** :
   - La requête SQL `INSERT INTO capteurs (...) VALUES (...)` est utilisée pour insérer des données dans la table `capteurs`.
   - Les valeurs sont passées sous forme de tuple (`values`) pour éviter les injections SQL.

3. **Validation des changements** :
   - La méthode `conn.commit()` est appelée après chaque insertion pour valider les changements dans la base de données.

4. **Fermeture de la connexion** :
   - La connexion et le curseur sont fermés avec `cursor.close()` et `conn.close()` pour libérer les ressources.

---

### **Étape 3 : Tester le script**

1. Exécute le script Python :
   ```bash
   python ton_script.py
   ```

2. Vérifie les données insérées dans la base de données MariaDB :
   - Connecte-toi à MariaDB :
     ```bash
     mysql -u iot_user -p
     ```
   - Sélectionne la base de données :
     ```sql
     USE iot_project;
     ```
   - Affiche les données de la table `capteurs` :
     ```sql
     SELECT * FROM capteurs;
     ```

   Tu devrais voir une sortie similaire à ceci :
   ```
   +----+----------+-------------------+-------------+----------+----------+---------------------+
   | id | nom      | adresse_mac       | temperature | humidite | batterie | horodatage          |
   +----+----------+-------------------+-------------+----------+----------+---------------------+
   |  1 | Capteur1 | D6:1C:BF:B7:76:62 |        22.5 |       60 |       80 | 2023-10-20 12:34:56 |
   |  2 | Capteur2 | D7:EF:13:27:15:29 |        25.0 |       55 |       75 | 2023-10-20 12:35:01 |
   |  3 | Capteur3 | D6:C6:C7:39:A2:E8 |        20.0 |       65 |       90 | 2023-10-20 12:35:05 |
   +----+----------+-------------------+-------------+----------+----------+---------------------+
   ```

---

### **Étape 4 : Intégrer avec ton projet Bluetooth**

Si tu veux insérer automatiquement les données des capteurs Bluetooth dans la base de données, tu peux intégrer ce script avec ton code existant. Par exemple :

1. **Modifier ton code Bluetooth pour insérer les données** :
   - Lorsque tu détectes un capteur Bluetooth et récupères ses données (température, humidité, etc.), appelle la fonction `insert_sensor_data()` pour insérer ces données dans la base.

2. **Exemple d'intégration** :
   ```python
   # Exemple d'intégration avec ton code Bluetooth
   from bluepy.btle import Scanner

   # Scanner les périphériques Bluetooth
   scanner = Scanner()
   devices = scanner.scan(5.0)  # Scanner pendant 5 secondes

   for device in devices:
       if device.addr.upper() in ["D6:1C:BF:B7:76:62", "D7:EF:13:27:15:29", "D6:C6:C7:39:A2:E8"]:
           # Exemple de données fictives (remplace par les vraies données)
           nom = "Capteur_" + device.addr[-2:]  # Nom basé sur l'adresse MAC
           adresse_mac = device.addr
           temperature = 22.5  # Remplace par la température réelle
           humidite = 60.0      # Remplace par l'humidité réelle
           batterie = 80        # Remplace par le niveau de batterie réel

           # Insérer les données dans la base
           insert_sensor_data(nom, adresse_mac, temperature, humidite, batterie)
   ```

---

### **Étape 5 : Points importants**

1. **Gestion des erreurs** :
   - Ajoute des blocs `try...except` pour gérer les erreurs de connexion ou d'insertion.

2. **Optimisation** :
   - Si tu insères beaucoup de données, utilise des transactions ou des requêtes groupées pour améliorer les performances.

3. **Sécurité** :
   - Utilise des paramètres pour éviter les injections SQL.
   - Ne stocke pas les mots de passe en clair dans le code. Utilise des variables d'environnement ou un fichier de configuration sécurisé.

---

