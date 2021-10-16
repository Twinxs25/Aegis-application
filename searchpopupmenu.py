from kivymd.uix.dialog import MDInputDialog


class SearchPopupMenu(MDInputDialog):
    title = 'Add Website URL'
    text_button_ok = 'Add'

    def __init__(self):
        super().__init__()
        self.size = [.9, .3]
        self.events_callback = self.block

    def block(self, *args):
        website_input = self.text_field.text
        print(website_input + " is blocked")
        redirect = "127.0.0.1"
        host_path = "C:\Windows\System32\drivers\etc\hosts"
        with open(host_path, "r+") as file:
            content = file.read()
            if website_input in content:
                pass
            else:
                file.write("\n" + redirect + "\t" + website_input + "\n")
