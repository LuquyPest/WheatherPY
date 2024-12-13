#install SSH
sudo systemctl enable ssh
sudo systemctl start ssh
sudo apt install -y proftpd
#install LIB for bluePY
sudo apt-get install -y python-pip libglib2.0-dev
sudo pip install bluepy