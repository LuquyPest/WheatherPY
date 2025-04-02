import smtplib
import datetime
from peewee import *
from email.mime.text import MIMEText
from BDD import *



# Paramètres SMTP
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = "btsciel.pi@gmail.com"
EMAIL_PASSWORD = "trpe ouui lmhy zuxs"


# Fonction pour envoyer un email
def send_alert(subject, message, receiver):
    msg = MIMEText(message)
    msg["From"] = EMAIL_SENDER
    msg["To"] = receiver
    msg["Subject"] = subject

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, receiver, msg.as_string())
        server.quit()
        print("Email envoyé avec succès.")
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email: {e}")

def check_alerts():
    sensor = Sensor.select().order_by(Sensor.id.desc()).first()
    alerts = []
    alerte=Alerte.select().first()      
    # Seuils d'alerte
    TEMP_MAX = alerte.tempmax
    TEMP_MIN = alerte.tempmin
    HUM_MAX = alerte.hummax
    HUM_MIN = alerte.hummin
    BATT_MIN = alerte.battmin        
    
    if sensor.temp > TEMP_MAX or sensor.temp < TEMP_MIN:
        print(f"Température critique: {sensor.temp}°C")
        alerts.append(f"Température critique: {sensor.temp}°C")
    if sensor.hum > HUM_MAX or sensor.hum < HUM_MIN:
        alerts.append(f"Humidité critique: {sensor.hum}%")
    if sensor.batt < BATT_MIN:
        alerts.append(f"Batterie faible: {sensor.batt}%")

    if alerts:
        send_alert("⚠️ Alerte Capteur", "\n".join(alerts),alerte.emailreceiver)

if __name__ == "__main__":
    check_alerts()