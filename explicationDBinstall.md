EXPLICATION création DB avec SH attention au varialble User à modifier
Pour inclure la création d'une table avec les colonnes spécifiques que tu as mentionnées (`id`, `nom`, `adresse_mac`, `Température`, `Humidité`, `Batterie`, `horodatage`), nous allons modifier le script précédent pour ajouter une commande SQL qui crée cette table après la création de la base de données.

Voici le script mis à jour :

---

### **Script Bash mis à jour**

```bash
#!/bin/bash

# Variables de configuration
DB_NAME="iot_project"                # Nom de la base de données
DB_USER="iot_user"                   # Nom de l'utilisateur
DB_PASSWORD="secure_password"        # Mot de passe de l'utilisateur
ROOT_PASSWORD="root_password"        # Mot de passe root pour MariaDB

# Couleurs pour les messages
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Fonction pour afficher un message
function print_message() {
    echo -e "${GREEN}$1${NC}"
}

# Fonction pour afficher un message d'erreur
function print_error() {
    echo -e "${RED}$1${NC}"
}

# Vérifier si l'utilisateur est root
if [ "$EUID" -ne 0 ]; then
    print_error "Ce script doit être exécuté en tant que root. Utilisez sudo."
    exit 1
fi

# Mise à jour des paquets
print_message "Mise à jour des paquets..."
apt update && apt upgrade -y

# Installation de MariaDB
print_message "Installation de MariaDB..."
apt install -y mariadb-server mariadb-client

# Démarrage et activation de MariaDB
print_message "Démarrage et activation de MariaDB..."
systemctl start mariadb
systemctl enable mariadb

# Sécurisation de l'installation de MariaDB
print_message "Sécurisation de l'installation de MariaDB..."
mysql_secure_installation <<EOF

y
$ROOT_PASSWORD
$ROOT_PASSWORD
y
y
y
y
EOF

# Création de la base de données, de l'utilisateur et de la table
print_message "Création de la base de données, de l'utilisateur et de la table..."
mysql -u root -p"$ROOT_PASSWORD" <<EOF
CREATE DATABASE $DB_NAME;
CREATE USER '$DB_USER'@'localhost' IDENTIFIED BY '$DB_PASSWORD';
GRANT ALL PRIVILEGES ON $DB_NAME.* TO '$DB_USER'@'localhost';
FLUSH PRIVILEGES;

USE $DB_NAME;

CREATE TABLE capteurs (
    id INT AUTO_INCREMENT PRIMARY KEY,       -- Identifiant unique
    nom VARCHAR(50) NOT NULL,                -- Nom du capteur
    adresse_mac VARCHAR(17) NOT NULL,        -- Adresse MAC du capteur
    temperature FLOAT,                       -- Température en degrés Celsius
    humidite FLOAT,                          -- Humidité en pourcentage
    batterie INT,                            -- Niveau de batterie en pourcentage
    horodatage DATETIME DEFAULT CURRENT_TIMESTAMP -- Horodatage de la mesure
);
EOF

# Vérification
if [ $? -eq 0 ]; then
    print_message "Base de données '$DB_NAME', utilisateur '$DB_USER' et table 'capteurs' créés avec succès."
    print_message "Vous pouvez maintenant vous connecter avec :"
    echo "  mysql -u $DB_USER -p"
else
    print_error "Une erreur s'est produite lors de la création de la base de données, de l'utilisateur ou de la table."
fi
```

---

### **Explications des modifications**

1. **Ajout de la création de la table `capteurs`** :
   - La commande SQL suivante est ajoutée après la création de la base de données et de l'utilisateur :
     ```sql
     CREATE TABLE capteurs (
         id INT AUTO_INCREMENT PRIMARY KEY,
         nom VARCHAR(50) NOT NULL,
         adresse_mac VARCHAR(17) NOT NULL,
         temperature FLOAT,
         humidite FLOAT,
         batterie INT,
         horodatage DATETIME DEFAULT CURRENT_TIMESTAMP
     );
     ```
   - **Colonnes de la table** :
     - `id` : Identifiant unique pour chaque enregistrement (clé primaire, incrémentation automatique).
     - `nom` : Nom du capteur (chaîne de caractères, obligatoire).
     - `adresse_mac` : Adresse MAC du capteur (chaîne de 17 caractères, obligatoire).
     - `temperature` : Température mesurée (nombre décimal).
     - `humidite` : Humidité mesurée (nombre décimal).
     - `batterie` : Niveau de batterie en pourcentage (entier).
     - `horodatage` : Date et heure de la mesure (par défaut, la date et l'heure actuelles).

2. **Structure SQL dans le script** :
   - Les commandes SQL sont exécutées dans un bloc `<<EOF ... EOF` pour automatiser leur exécution.

3. **Vérification de la création** :
   - Le script vérifie si les commandes SQL ont été exécutées avec succès et affiche un message approprié.

---

### **Exécution du script**

1. Sauvegarde le script dans un fichier, par exemple `setup_mariadb_with_table.sh` :
   ```bash
   nano setup_mariadb_with_table.sh
   ```

2. Colle le contenu du script dans le fichier.

3. Rends le script exécutable :
   ```bash
   chmod +x setup_mariadb_with_table.sh
   ```

4. Exécute le script avec `sudo` :
   ```bash
   sudo ./setup_mariadb_with_table.sh
   ```

---

### **Résultat attendu**

1. MariaDB sera installé et démarré.
2. Une base de données `iot_project` sera créée.
3. Un utilisateur `iot_user` sera créé avec le mot de passe `secure_password`.
4. Une table `capteurs` sera créée dans la base de données `iot_project` avec les colonnes spécifiées.

---

### **Tester la configuration**

1. Connecte-toi à MariaDB avec l'utilisateur créé :
   ```bash
   mysql -u iot_user -p
   ```

2. Saisis le mot de passe (`secure_password`).

3. Sélectionne la base de données :
   ```sql
   USE iot_project;
   ```

4. Vérifie que la table a été créée :
   ```sql
   SHOW TABLES;
   ```

   Tu devrais voir une sortie comme :
   ```
   +------------------+
   | Tables_in_iot_project |
   +------------------+
   | capteurs         |
   +------------------+
   ```

5. Affiche la structure de la table :
   ```sql
   DESCRIBE capteurs;
   ```

   Tu devrais voir une sortie comme :
   ```
   +-------------+--------------+------+-----+-------------------+----------------+
   | Field       | Type         | Null | Key | Default           | Extra          |
   +-------------+--------------+------+-----+-------------------+----------------+
   | id          | int          | NO   | PRI | NULL              | auto_increment |
   | nom         | varchar(50)  | NO   |     | NULL              |                |
   | adresse_mac | varchar(17)  | NO   |     | NULL              |                |
   | temperature | float        | YES  |     | NULL              |                |
   | humidite    | float        | YES  |     | NULL              |                |
   | batterie    | int          | YES  |     | NULL              |                |
   | horodatage  | datetime     | YES  |     | CURRENT_TIMESTAMP |                |
   +-------------+--------------+------+-----+-------------------+----------------+
   ```

---

