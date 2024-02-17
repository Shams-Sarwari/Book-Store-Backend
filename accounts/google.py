from google.auth.transport import requests
from google.oauth2 import id_token


class Google:

    @staticmethod
    def validate(auth_token):
        try:
            idinfo = id_token.verify_oauth2_token(auth_token, requests.Request)

            if "accounts.google.com" in id_token["iss"]:
                return idinfo
        except:
            raise "The token is invalid or expired"
