import json
import requests

FIREBASE_API_TOKEN = "AAAARYpaAJs:APA91bHF_F80qIHSm6MCiPxjuSiUQbUp3i7M_-jH4zaRP-EjyH9tXCI5fhxvRZjNPxVv_ZRESlbuoMNLOPgl72v9Xx33yx1na09BX_8OnVKlZ1-M-SQAKZgKtltHxXwI2yLhrUwm_rQ9"

class FirebaseServer:
    URL = 'https://fcm.googleapis.com/fcm/send'
    def __init__(self, token):
        self.__token = token


    def send(self, title, body, registration_ids):
        n_body = {
            "notification":  {
                "title": title,
                "body": body,
                "icon" : "myicon",
                "click_action": "https://www.google.ro",
                "sound" : "res_notif_sound",
                "content_available": "true"
            },
            "registration_ids": registration_ids
        }

        headers = {"Content-Type":"application/json",
        "Authorization": "key=" + self.__token}

        response = requests.post(self.URL, data=json.dumps(n_body), headers=headers)

        print ("response: " + response.text)
        