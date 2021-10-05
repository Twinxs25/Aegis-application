from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.snackbar import Snackbar
from kivy.metrics import dp
from kivy.core.window import Window
from searchpopupmenu import SearchPopupMenu
from os.path import join
from credentials import Credentials
from kivy.graphics import Color, RoundedRectangle
Window.size = (450, 680)

class LoginWindow(Screen):
    pass
    
class MainMenu(Screen):
    pass

class WindowManager(ScreenManager):
    pass

class Aegis(MDApp):
    search = None


    def build(self):
    
        kv = Builder.load_file("main.kv")

        self.credentials = Credentials() 
        self.search = SearchPopupMenu()

        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": f"Website {i + 1}",
                "height": dp(56),
                "on_release": lambda x=f"Webiste {i + 1}": self.menu_callback(x),
            } for i in range(5)
        ]
        self.menu = MDDropdownMenu(
            items=menu_items,
            width_mult=3,
        )

        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Gray"
        return kv

    def on_start(self):
    
        try:
            with open("refresh_token.txt", 'r') as f:
                refresh_token = f.read()
            
            # Use refresh token to get a new idToken
            id_token, local_id = self.credentials.exchange_refresh_token(refresh_token)

            print("https://aegis-5353f-default-rtdb.asia-southeast1.firebasedatabase.app/" + local_id + ".json?auth=" + id_token)

            self.change_screen("main_menu")
        except:
            pass

    def callback(self, button):
        self.menu.caller = button
        self.menu.open()

    def menu_callback(self, text_item):
        self.menu.dismiss()
        Snackbar(text=text_item).open()

    def change_screen(self, screen_name):

        screen_manager = self.root.ids['screen_manager']
        screen_manager.current = screen_name

Aegis().run()
