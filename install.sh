#install SSH
sudo apt update
sudo apt upgrade
sudo systemctl enable ssh
sudo systemctl start ssh
#install FTP
sudo apt install proftpd
#install LIB for bluePY
sudo apt-get install python-pip libglib2.0-dev
sudo pip install bluepy