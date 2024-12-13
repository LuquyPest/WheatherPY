#install SSH
sudo systemctl enable ssh
sudo systemctl start ssh
sudo apt install -y proftpd
#install pip for installation of bluePY
sudo apt install -y pip 
pip install bluepy
#create virtual environements "weatherpy"
python3 -m venv weatherpy
#activate venv
. weatherp/bin/activate
