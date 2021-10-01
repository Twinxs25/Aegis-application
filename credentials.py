import requests
import json
from kivy.app import App
from requests.api import request
class Credentials():

    wak = "AIzaSyAE13BsICHm8LGMLYJ1ZTY71zGbJopY-ss" # WEB API KEY

    def sign_up(self, email, password):

        app = App.get_running_app()

        # Sends email and password to Firebase
        # Firebase will returns idToken, email, refreshToken, localId
        signup_url = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/signupNewUser?key=" + self.wak
        signup_payload = {"email": email, "password": password, "returnSecureToken": True}
        sign_up_request = requests.post(signup_url, data=signup_payload)
        print(sign_up_request.ok)
        print(sign_up_request.content.decode())
        sign_up_data = json.loads(sign_up_request.content.decode())

        if sign_up_request.ok == True:
            refresh_token = sign_up_data['refreshToken']
            localId = sign_up_data['localId']
            idToken = sign_up_data['idToken']

            # Save refreshToken to a file
            with open("refresh_token.txt", "w") as f:
                f.write(refresh_token)

            # Save localId to a variable in Aegis app class
            # Save idToken to a variable in Aegis app class
            app.local_id = localId
            app.id_token = idToken


            # Create new key in database from localId
            # Get User ID
            # Default avatar
            # Website list
            my_data = '{"avatar": "aegis_logo.png", "User ID" : "", "website_list" : ""}'
            post_request = requests.patch("https://aegis-5353f-default-rtdb.asia-southeast1.firebasedatabase.app/" + localId + ".json?auth=" + idToken,
                            data = my_data)
            print(post_request.ok)
            print(json.loads(post_request.content.decode()))

            

        if sign_up_request.ok == False:
            error_data = json.loads(sign_up_request.content.decode())
            error_message = error_data["error"]["message"] 
            app.get_running_app().root.ids['login_screen'].ids['login_message'].text = error_message

        pass

    def log_in(self):
        pass

        