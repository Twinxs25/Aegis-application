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

            app.change_screen("main_menu")    

        if sign_up_request.ok == False:
            error_data = json.loads(sign_up_request.content.decode())
            error_message = error_data["error"]["message"] 
            app.get_running_app().root.ids['login_screen'].ids['login_message'].text = error_message

    def sign_in_existing_user(self, email, password):
        """Called if a user tried to sign up and their email already existed."""
        signin_url = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key=" + self.wak
        signin_payload = {"email": email, "password": password, "returnSecureToken": True}
        signin_request = requests.post(signin_url, data=signin_payload)
        sign_up_data = json.loads(signin_request.content.decode())
        app = App.get_running_app()

        if signin_request.ok == True:
            refresh_token = sign_up_data['refreshToken']
            localId = sign_up_data['localId']
            idToken = sign_up_data['idToken']
            # Save refreshToken to a file
            with open(app.refresh_token_file, "w") as f:
                f.write(refresh_token)

            # Save localId to a variable in main app class
            # Save idToken to a variable in main app class
            app.local_id = localId
            app.id_token = idToken

            
            app.on_start()
        elif signin_request.ok == False:
            error_data = json.loads(signin_request.content.decode())
            error_message = error_data["error"]['message']
            app.root.ids['login_screen'].ids['login_message'].text = "EMAIL EXISTS - " + error_message.replace("_", " ")

    def exchange_refresh_token(self, refresh_token):
        refresh_url = "https://securetoken.googleapis.com/v1/token?key=" + self.wak
        refresh_payload = '{"grant_type": "refresh_token", "refresh_token": "%s"}' % refresh_token
        refresh_req = requests.post(refresh_url, data=refresh_payload)
        print("refresh ok?", refresh_req.ok)
        print(refresh_req.json())

        id_token = refresh_req.json()['id_token']
        local_id = refresh_req.json()['user_id']
        return id_token, local_id

        