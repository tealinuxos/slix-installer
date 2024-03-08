from textual import on
from textual.containers import Horizontal, Vertical, Center
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Input, Label, Button, Footer
import subprocess, os, sys

class Form(App):
    #CSS_PATH = "nyoba.tcss"
    
    BINDINGS = [
        Binding("ctrl+c","quit","Exit Program"),
        ]
    
    def compose(self) -> ComposeResult:
        yield Input(placeholder="Input package name here ...")
        yield Horizontal(
            Button("install", id="btn_install"),
            Button("search", id="btn_search"),
            Button("exit", id="btn_exit"),
        )
        yield Footer()
    
    @on(Button.Pressed, "#btn_install")
    @on(Input.Submitted)
    def accept_package(self, event: Button.Pressed):
        input = self.query_one(Input)
        if not input.value:
            self.mount(Label("[-] Please input a package name."))
            return
        package = input.value
        self.mount(Label("======================================="))
        self.mount(Label(f"[*] installing {package} ..."))
        self.mount(Label("======================================="))
        try:
            p = subprocess.run(["sudo", "pacman", "-S", package, "--noconfirm"], shell=False, capture_output=True, text=True)
            if f"extra/{package}" in p.stdout and "Arming ConditionNeedsUpdate" in p.stdout:
                self.mount(Label("======================================="))
                self.mount(Label(f"[*] installing {package} done"))
                self.mount(Label("======================================="))
            else:
                self.mount(Label("======================================="))
                self.mount(Label(f"[-] installing {package} failed"))
                self.mount(Label("======================================="))
        except subprocess.CalledProcessError as e:
            self.mount(Label("======================================="))
            self.mount(Label(f"[-] Failed to install {package}: {e}"))
            self.mount(Label("======================================="))
        input.value = ""
    
    @on(Button.Pressed, "#btn_search")
    def search_package(self, event: Button.Pressed):
        input = self.query_one(Input)
        if not input.value:
            self.mount(Label("[-] Please input a package name."))
            return
        package = input.value
        result = self.search_package_local(package)
        if result:
            for output in result:
                self.mount(Label("======================================="))
                self.mount(Label(f"[*] Package Name:  {output['name']}"))
                self.mount(Label(f"[*] Package Status:  {output['status']}"))
                self.mount(Label(f"[*] Package Version:  {output['version']}"))
                self.mount(Label(f"[*] Package Description:  {output['description']}"))
                self.mount(Label("======================================="))
        else:
            self.mount(Label(f"[-] Package {package} not found."))

    def search_package_local(self, package):
        try:
            output = subprocess.check_output(["pacman", "-Ss", f"{package}"], text=True)
            lines = output.splitlines()
            package_info = []
            for i in range(0, len(lines), 2):
                name_line = lines[i].strip()
                desc_line = lines[i+1].strip()
                name, version = name_line.split(' ', maxsplit=1)
                description = desc_line[desc_line.find(':')+1:].strip()
                if "[installed]" in output:
                    status = "installed"
                else:
                    status = "not installed"
                package_info.append({
                    "name": name,
                    "version": version,
                    "description": description,
                    "status": status
                })
            return package_info
        except subprocess.CalledProcessError:
            return []
    @on(Button.Pressed, "#btn_exit")    
    def action_quit(self):
        self.mount(Label("[!] Exiting the program"))
        #time.sleep(10)
        self.exit()

if __name__ == "__main__":
    uid = os.getuid()
    if uid == 0:
        os.setuid(0)
        pass
    else:
        print(f"[!] You must run program with sudo first ...\n[*] exp: sudo python3 {__file__}")
        sys.exit(0)
    Form().run()