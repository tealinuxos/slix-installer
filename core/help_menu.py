from core.color import co
from core.banner import ban
import os

### 2.2 show help ###
def help():
    os.system("clear")
    ban()
    print(f"""
    {co.ye}{co.bo}Tea Linux Installer Beta Version{co.re}
    
    options:
    help\t\t\tShow all command
    partition\t\t\tShow all partition on your device
    set efi /dev/(device name)\tSetting your device partition to be place for install bootloader
    set /dev/(device name)\tSetting your device partition to be place for install Tea Linux
    set user (username)\t\tMake default user after installation
    set hostname (hostname)\tSetting hostname of your machine
    set root pass\tSetting your root password (opsionale)
    set package (package)\tList package that you want install
    set DE\t\t\tSetting your desktop environment
    set time (region) (city)\tSetting localtime
    set language (LocaleCode)\tSetting your langueage machine
    set keymap (keymapcode)\tSetting your your keymaps machine
    list time zone\t\tShow all time zone
    list city (region)\t\tShow all city in the region
    list keymaps\t\tShow all keyboard layout
    show options\t\tShow all options that you select
    clear\t\t\tclear prompt
    exit\t\t\tExit installer   
    """)