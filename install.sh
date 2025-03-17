#install SSH
sudo systemctl enable ssh
sudo systemctl start ssh
sudo apt install -y proftpd
# Install MariaDB
sudo apt install mariadb-server mariadb-client -y
sudo systemctl start mariadb
sudo systemctl enable mariadb
#install pip for installation of bluePY
sudo apt install -y pip 
#create virtual environements "weatherpy"
python3 -m venv weatherpy
#activate venv
. weatherpy/bin/activate
pip install bluepy
# Install de fast api
pip install fastapi
# Install de uvicorn
pip install uvicorn
# Install Peewee
pip install peewee pymysql
# Créa BDD
DB_NAME="bdd_weath"
DB_USER="pi"
DB_PASS="test"
sudo mysql -u root bdd_weath <<EOF
CREATE DATABASE IF NOT EXISTS $DB_NAME CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS '$DB_USER'@'localhost' IDENTIFIED BY '$DB_PASS';
GRANT ALL PRIVILEGES ON $DB_NAME.* TO '$DB_USER'@'localhost';
FLUSH PRIVILEGES;
SHOW DATABASES;
EOF
echo okay
sudo /home/pi/Desktop/WheatherPY/weatherpy/bin/python3.11 /home/pi/Desktop/WheatherPY/BDD.py
sudo /home/pi/Desktop/WheatherPY/weatherpy/bin/python3.11 /home/pi/Desktop/WheatherPY/meteo.py
