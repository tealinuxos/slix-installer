from textual.app import App, ComposeResult
from textual.containers import Container, VerticalScroll, Grid
from textual.screen import ModalScreen
from textual.widgets import Static, Button, ContentSwitcher, Label, Footer
from textual.widget import Widget
from textual.binding import Binding
from textual import on


class MetuSu(ModalScreen):
    def compose(self) -> ComposeResult:
        with Grid(id="dialog"):
            yield Label("Are you sure?", id="question")
            yield Button("Quit", id="metu")
            yield Button("Cancel", id="rakmetu")
        
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "metu":
            self.app.exit()
        else:
            self.app.pop_screen()

class Home(Widget):
    def on_mount(self) -> None:
        self.tampil()
    def tampil(self) -> None:
        yield Static("""
                          ______
                       .-'      '-.
                      /            \\
                     |              |
                     |,  .-.  .-.  ,|
                     | )(_o/  \o_)( |
                     |/     /\     \|
           (@_       (_     ^^     _)
      _     ) \_______\__|IIIIII|__/__________________________
     (_)@8@8{}<________|-\IIIIII/-|___________________________>
            )_/        \          /
           (@           `--------`
                    Wellcome to the installer

                             """)


class Tea(App[None]):
    BINDINGS = [
        Binding("q","tombol_metu", "Quit", priority=True)
    ]

    CSS_PATH = "pake.tcss"

    def compose(self) -> ComposeResult:
        with VerticalScroll(classes="scrollsu",id="sidebar"):
            yield Label("Menu")
            yield Button("Partition", id="SettingPartition") # setting partition for installation and for efi 
            yield Button("User", id="SettingUser") # setting user, root pass, hostname
            yield Button("Time Zone", id="SettingTime") # setting time zone, and show city,  country
            yield Button("Keymap", id="SettingKeyboardMapping") # setting keymap and show all the keymap code
            yield Button("Package", id="SettingPackage") # setting package that will be install 
            yield Button("Desktop Env", id="SettingDE") # setting Desktop Enviroment and show all support DE 
            yield Button("Install", id="InstallTea") # button to install tea linux but show all the options was selected before
            
        with Container(id="badan"):
            yield Label("Tea Linux Installer")
            with ContentSwitcher(initial="dashboard", classes="badan"):
                yield Home(id="dashboard")
                yield Static("Page bagian paritisi coeg", id="SettingPartition")
                yield Static("Page bagian user coeg", id="SettingUser")
                yield Static("Page bagian time coeg", id="SettingTime")
                yield Static("Page bagian keymap coeg", id="SettingKeyboardMapping")
                yield Static("Page bagian packages coeg", id="SettingPackage")
                yield Static("Page bagian Desktop Enviroment coeg", id="SettingDE")
                yield Static("Page bagian install coeg", id="InstallTea")
            yield Footer()
    
    def action_tombol_metu(self) -> None:
        self.push_screen(MetuSu())
        
    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.query_one(ContentSwitcher).current = event.button.id
    
    # def on_mount(self) -> None:
        # partisi_su = self.query_one(Static)

if __name__ == "__main__":
    app = Tea()
    app.run()
