import requests
from datetime import datetime, timedelta


def temperature_merignac():
    # Clé API (remplace avec la tienne)
    API_KEY = "eyJ4NXQiOiJZV0kxTTJZNE1qWTNOemsyTkRZeU5XTTRPV014TXpjek1UVmhNbU14T1RSa09ETXlOVEE0Tnc9PSIsImtpZCI6ImdhdGV3YXlfY2VydGlmaWNhdGVfYWxpYXMiLCJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJFZG91YXJkOTlAY2FyYm9uLnN1cGVyIiwiYXBwbGljYXRpb24iOnsib3duZXIiOiJFZG91YXJkOTkiLCJ0aWVyUXVvdGFUeXBlIjpudWxsLCJ0aWVyIjoiVW5saW1pdGVkIiwibmFtZSI6IkRlZmF1bHRBcHBsaWNhdGlvbiIsImlkIjoyNjMzNiwidXVpZCI6IjQ3Y2Y5MGY1LTRlZTEtNDg5Mi05MWE4LTg0MWY1NTE4MDYzYyJ9LCJpc3MiOiJodHRwczpcL1wvcG9ydGFpbC1hcGkubWV0ZW9mcmFuY2UuZnI6NDQzXC9vYXV0aDJcL3Rva2VuIiwidGllckluZm8iOnsiNTBQZXJNaW4iOnsidGllclF1b3RhVHlwZSI6InJlcXVlc3RDb3VudCIsImdyYXBoUUxNYXhDb21wbGV4aXR5IjowLCJncmFwaFFMTWF4RGVwdGgiOjAsInN0b3BPblF1b3RhUmVhY2giOnRydWUsInNwaWtlQXJyZXN0TGltaXQiOjAsInNwaWtlQXJyZXN0VW5pdCI6InNlYyJ9fSwia2V5dHlwZSI6IlBST0RVQ1RJT04iLCJzdWJzY3JpYmVkQVBJcyI6W3sic3Vic2NyaWJlclRlbmFudERvbWFpbiI6ImNhcmJvbi5zdXBlciIsIm5hbWUiOiJBUk9NRSIsImNvbnRleHQiOiJcL3B1YmxpY1wvYXJvbWVcLzEuMCIsInB1Ymxpc2hlciI6ImFkbWluX21mIiwidmVyc2lvbiI6IjEuMCIsInN1YnNjcmlwdGlvblRpZXIiOiI1MFBlck1pbiJ9LHsic3Vic2NyaWJlclRlbmFudERvbWFpbiI6ImNhcmJvbi5zdXBlciIsIm5hbWUiOiJEb25uZWVzUHVibGlxdWVzQ2xpbWF0b2xvZ2llIiwiY29udGV4dCI6IlwvcHVibGljXC9EUENsaW1cL3YxIiwicHVibGlzaGVyIjoiYWRtaW5fbWYiLCJ2ZXJzaW9uIjoidjEiLCJzdWJzY3JpcHRpb25UaWVyIjoiNTBQZXJNaW4ifV0sImV4cCI6MTgzODI1OTYyMywidG9rZW5fdHlwZSI6ImFwaUtleSIsImlhdCI6MTc0MzU4NjgyMywianRpIjoiZTkyMDRlYmYtNTA1Yi00NTBhLWJkZTEtMzY4MTEyM2U3Y2M4In0=.OhPwTrMiYfE1GSDmNJ-nk9yo6T80mqDm5monQrQvFMQfy-h5Jb9xaSUaNWDruPOpJsOPAF_yiGL_HW7QjUuNFe6OzSQX-uF2vxgEmhqy4q4A6KQNAiFYL6YPWlL-UlH5DXHyfMongGMvMDB_aDBj9dUzcy7w4PQbyuhDLPIfSHkVvDHCvo-JyetLvsKxJ7OAbQu_SIRyPhJF7NSGUG8n-lJ52R0rMtj83MNI9yVqIFyHKUOXF0Du_pHf0MEKS701IahLc-K2-ROodNhU7_rA3iTctOUU78tty0N4qBhbqVxrFi8VE34vnDoewDVFzpWWN0Kqr4_p04jR26LR6g2WHA=="

    # Calcul de l'heure actuelle - 4 heures
    heure_actuelle = datetime.now()
    heure_h4 = heure_actuelle - timedelta(hours=2)
    formatted_date = heure_h4.strftime("%Y-%m-%dT%H:00:00Z")

    # URL pour commander les données
    url_commande = (
        "https://public-api.meteofrance.fr/public/DPClim/v1/commande-station/horaire"
    )
    params_commande = {
        "id-station": "33281001",  # ID de la station de Mérignac
        "date-deb-periode": formatted_date,
        "date-fin-periode": formatted_date,
    }
    headers = {"accept": "*/*", "apikey": API_KEY}
    temperature = None
    try:
        # Envoi de la requête pour obtenir l'ID de commande
        response = requests.get(url_commande, headers=headers, params=params_commande)
        data = response.json()

        if "code" in data and data["code"] == "900901":
            raise Exception("Authentification échouée : Vérifie la clé API.")

        # Récupération de l'ID de commande
        id_commande = data.get("elaboreProduitAvecDemandeResponse", {}).get("return")
        if not id_commande:
            raise Exception(
                "L'ID de commande est introuvable dans la réponse de l'API."
            )

        # URL pour récupérer le fichier de données
        url_fichier = f"https://public-api.meteofrance.fr/public/DPClim/v1/commande/fichier?id-cmde={id_commande}"

        # Télécharger le fichier
        response_fichier = requests.get(url_fichier, headers=headers)
        fichier_texte = response_fichier.text

        # Extraction de la température
        lignes = fichier_texte.split("\n")
        if len(lignes) < 2:
            raise Exception(
                "Le fichier de réponse ne contient pas suffisamment de données."
            )

        donnees = lignes[1].split(";")
        if len(donnees) < 11:
            raise Exception("Format des données inattendu.")

        temperature = donnees[10]
        print(temperature)

    except Exception as e:
        print(f"Erreur lors de la récupération des données : {e}")
    return temperature


temperature_merignac()
