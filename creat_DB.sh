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
