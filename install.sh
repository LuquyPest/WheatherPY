# #install SSH
# sudo systemctl enable ssh
# sudo systemctl start ssh
# sudo apt install -y proftpd
# # Install MariaDB
# sudo apt install mariadb-server mariadb-client -y
# sudo systemctl start mariadb
# sudo systemctl enable mariadb
# #install pip for installation of bluePY
# sudo apt install -y pip 
# #create virtual environements "weatherpy"
# python3 -m venv weatherpy
#activate venv
. weatherpy/bin/activate
# sudo apt install libglib2.0-dev -y
# pip install bluepy
# # Install de fast api
# pip install fastapi
# # Install de uvicorn
# pip install uvicorn
# # Install Jinja
# pip install jinja2
# # Install Peewee
# pip install peewee pymysql
pip install python-multipart
pip install requests
# Créa BDD
DB_NAME="bdd_weath"
DB_USER="pi"
DB_PASS="test"
echo okay1
sudo mysql -u root <<EOF
DROP DATABASE IF EXISTS $DB_NAME;
CREATE DATABASE IF NOT EXISTS $DB_NAME CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS '$DB_USER'@'localhost' IDENTIFIED BY '$DB_PASS';
GRANT ALL PRIVILEGES ON $DB_NAME.* TO '$DB_USER'@'localhost';
FLUSH PRIVILEGES;
SHOW DATABASES;
EOF
echo okay2
sudo /home/pi/Desktop/WheatherPY/weatherpy/bin/python3.11 /home/pi/Desktop/WheatherPY/BDD.py
uvicorn website:app --reload --host 0.0.0.0 --port 8000 &
sudo /home/pi/Desktop/WheatherPY/weatherpy/bin/python3.11 /home/pi/Desktop/WheatherPY/meteo.py
