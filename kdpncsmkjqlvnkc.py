import smtplib
import datetime
from peewee import *
from email.mime.text import MIMEText

# Connexion à la base de données
db = MySQLDatabase('bdd_weath', user='pi', password='test', host='localhost', port=3306)

class Sensor(Model):
    mac = CharField()
    temp = FloatField()
    hum = FloatField()
    batt = IntegerField()
    heurodatage = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db

# Seuils d'alerte
TEMP_MAX = 30.0
TEMP_MIN = 0.0
HUM_MAX = 80.0
HUM_MIN = 20.0
BATT_MIN = 20

# Paramètres SMTP
SMTP_SERVER = "smtp.office365.com"
SMTP_PORT = 587
EMAIL_SENDER = "lylian.fredon@daryu.xyz"
EMAIL_PASSWORD = "Pl0mbier.070000"
EMAIL_RECEIVER = "destinataire@example.com"

# Fonction pour envoyer un email
def send_alert(subject, message):
    msg = MIMEText(message)
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg["Subject"] = subject

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        server.quit()
        print("Email envoyé avec succès.")
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email: {e}")

def check_alerts():
    for sensor in Sensor.select():
        alerts = []
        if sensor.temp > TEMP_MAX or sensor.temp < TEMP_MIN:
            alerts.append(f"Température critique: {sensor.temp}°C")
        if sensor.hum > HUM_MAX or sensor.hum < HUM_MIN:
            alerts.append(f"Humidité critique: {sensor.hum}%")
        if sensor.batt < BATT_MIN:
            alerts.append(f"Batterie faible: {sensor.batt}%")

        if alerts:
            send_alert("⚠️ Alerte Capteur", "\n".join(alerts))

if __name__ == "__main__":
    check_alerts()
