from kivymd.uix.dialog import MDInputDialog


class SearchPopupMenu(MDInputDialog):
    title = 'Add Website URL'
    text_button_ok = 'Add'

    def __init__(self):
        super().__init__()
        self.size = [.9, .3]
        self.events_callback = self.callback

    def callback(self, *args):
        website_url = self.text_field.text
        print(website_url)
