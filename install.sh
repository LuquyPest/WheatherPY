#install SSH
sudo apt update
sudo systemctl enable ssh
sudo systemctl start ssh
sudo apt install proftpd
#install LIB for bluePY
sudo apt-get install python-pip libglib2.0-dev
sudo pip install bluepy