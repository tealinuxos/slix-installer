from core.banner import ban # for show the banner
from core.color import co # to use color 
from core.show_partition import part # to  print partition info
from core.set_device import set_device # to set partition
from core.set_efi import set_device_efi # to set efi partition
from core.list_time_zone import list_time_zones # show the time zone
from core.list_city import list_time_city # show the city zone
from core.list_language import list_languages # show the language
from core.install import install_tea # lib for install tea linux
from core.list_keymap import list_keymaps  # for show all keymaps
from core.print_keymap import print_keymaps # print all keymap from list_keymaps
from core.help_menu import help # to show help banner
import os # do execute some command in python, everyone know it

""" 
code by x0r, this code is nasty anyway
"""

### main function i think, bcz this the prompt###
def teaprompt():
    selected_device = None
    selected_device_efi = None
    selected_time_region = None
    selected_time_city = None
    selected_lang = None
    selected_keymap = None
    selected_hostname = None
    selected_root_pass = None
    selected_username = None
    selected_user_pass = None
    package_list = None
    selected_DE = None
    os.system("clear")
    ban()
    print(f"{co.ye}Welcome to TeaLinux Installer. Type 'help' to see all command and type 'exit' to quit.{co.re}\n")
    while True:
        # the prompt
        user_input = input("Tea Installer > ")
        
        # if user type exit
        if user_input.lower() == 'exit':
            print(f"{co.r}[!] Exiting Tea Linux Installer...{co.re}")
            break
        
        # if user type help
        elif user_input.lower() == 'help':
            help()
            
        # if user type partition
        elif user_input.lower() == 'partition':
            device_names = part()
            
        # if user type set /dev/(device name)
        elif user_input.lower().startswith('set /dev/'):
            selected_device = set_device(user_input[9:], device_names)
        
        elif user_input.lower().startswith('set efi /dev/'):
            selected_device_efi = set_device_efi(user_input[8:], device_names) 

        # if user type install
        elif user_input.lower() == 'install':
            if selected_device and selected_device_efi and selected_time_city and selected_time_region and selected_lang and selected_keymap and selected_hostname and selected_username and selected_user_pass and package_list:
                install_tea(selected_device, selected_device_efi, selected_time_region, selected_time_city, selected_lang, selected_keymap, selected_hostname, selected_username, selected_user_pass, selected_root_pass, selected_DE, package_list)
            else:
                print(f"{co.r}[!] select partition first !{co.re}")
                
        # if user type list time zone
        elif user_input.lower() == 'list time zone':
            list_time_zones()
            
        # set root pass
        elif user_input.lower() == 'set root pass':
            selected_root_pass = input("Tea Installer[root pass] > ")
            if selected_root_pass:
                print(f"{co.g}[*] Your root password has set{co.re}")
            else:
                print(f"{co.r}[!] You didn't input anything{co.re}")
                
        # set user & pass
        elif user_input.lower() == 'set user':
            selected_username= input("Tea Installer[username] > ")
            if selected_username:
                print(f"{co.g}[*] Your username is {selected_username}{co.re}")
            else:
                print(f"{co.r}[!] You didn't input anything{co.re}")
            selected_user_pass= input("Tea Installer[password] > ")
            if selected_user_pass:
                print(f"{co.g}[*] Your password for user {selected_username} is set ..{co.re}")
            else:
                print(f"{co.r}[!] You didn't input anything{co.re}")
            
        # if user type clear
        elif user_input.lower() == 'clear':
            os.system("clear")
            ban()
            
        # if user type list keymaps
        elif user_input.lower() == 'list keymaps':
            keymap_list = list_keymaps()
            print_keymaps(keymap_list)
            
        # if user type set de, for select deesktop env, and this is opsional, user can setup and no
        elif user_input.lower().startswith("set de"):
            tokens = user_input.split(' ', 2)
            support = ["gnome", "xfce", "kde"]
            if len(tokens) == 3:
                _, _, de = tokens
                if  de in support:
                    selected_DE = de
                    print(f"{co.g}[*]  Set your Desktop Enviroment to {selected_DE}{co.re}")
                else:
                    print(f"{co.r}[!] you set to {de}, that Desktop Enviroment is not support for now{co.re}")
            else:
                print(f"{co.g}[*] List Desktop Enviroment that we supported to install (for now): {co.re}")
                for i in support:
                    print(f"[*] {i}")
                print(f"[!]  Invalid {co.r}'set de'{co.re} command format. Please use {co.g}'set de DesktopEnviroment'{co.re}.")
            
        # if user set the keymaps
        elif user_input.lower().startswith('set keymap'):
            tokens = user_input.split(' ', 3)
            if len(tokens) == 3:
                _, _, keymap = tokens
                selected_keymap = keymap
                keymap_list = list_keymaps()
                if keymap in keymap_list:
                    print(f"{co.g}[*] Keymap set to {selected_keymap}{co.re}")
                else:
                    print(f"{co.ye}[!] Invalid keymap code. Please select a valid keymap.{co.re}")
            else:
                print(f"[!] Invalid {co.r}'set keymap'{co.re} command format. Please use {co.g}'set keymap keymap_code'{co.re}.")
            
        # if user input package that will be installed
        elif user_input.lower().startswith('set package'):
            tokens = user_input.split(' ', 2)
            if len(tokens) == 3:
                _, _, packages = tokens
                package_list = packages.split()
                print(f"{co.g}[*] Package that will be install : {', '.join(package_list)}{co.re}")
            else:
                print(f"[!] Invalid {co.r}'set package'{co.re} command format. Please use {co.g}'set package Package1 Package2 ...'{co.re}.")

        # if user type set time Region City
        elif user_input.lower().startswith('set time'):
            tokens = user_input.split(' ', 3)
            if len(tokens) == 4:
                _, _, region, city = tokens
                selected_time_region = region
                selected_time_city = city
                print(f"{co.g}[*] Time set to {region}/{city} ..{co.re}")
            else:
                print(f"[!] Invalid {co.r}'set time'{co.re} command format. Please use {co.g}'set time Region City'{co.re}.")
                
        # if user type set language
        elif user_input.lower().startswith('set language'):
            tokens = user_input.split(' ', 3)
            if len(tokens) == 2:
                list_languages()
            elif len(tokens) == 3:
                _, _, locale = tokens
                selected_lang = locale
                print(f"{co.g}[*] Language set to {selected_lang} ..{co.re}")
            else:
                print(f"[!] Invalid {co.r}'set language'{co.re} command format. Please use {co.ye}'set language'{co.re} to list or {co.g}'set language LocaleCode'{co.re} to set.")
                
        # if user type list city
        elif user_input.lower().startswith('list city'):
            tokens = user_input.split(' ', 2)
            if len(tokens) == 3:
                _, _, cityin = tokens
                list_time_city(cityin)
            else:
                print(f"[!]  Invalid {co.r}'list city'{co.re} command format. Please use {co.g}'list city Regions'{co.re}.")
                
        # if user set hostname        
        elif user_input.lower().startswith('set hostname'):
            tokens = user_input.split(' ', 3)
            if len(tokens) == 3:
                _, _, hostname = tokens
                selected_hostname = hostname
                print(f"{co.g}[*] Hostname set to {selected_hostname}{co.re}")
            else:
                print(f"[!] Invalid {co.r}'set hostname'{co.re} command format. Please use {co.g}'set hostname YourHostName'{co.re}.")
        
        elif user_input.lower().startswith('show options'):
            print(f"{co.g}[*] partition for Tea install:\t{co.re}{co.ye}{selected_device}{co.re}")
            print(f"{co.g}[*] partition for EFI:\t\t{co.re}{co.ye}{selected_device_efi}{co.re}")
            print(f"{co.g}[*] region time:\t\t{co.re}{co.ye}{selected_time_region}{co.re}")
            print(f"{co.g}[*] city time:\t\t\t{co.re}{co.ye}{selected_time_city}{co.re}")
            print(f"{co.g}[*] language:\t\t\t{co.re}{co.ye}{selected_lang}{co.re}")
            print(f"{co.g}[*] keymaps:\t\t\t{co.re}{co.ye}{selected_keymap}{co.re}")
            print(f"{co.g}[*] root password:\t\t{co.re}{co.ye}{selected_root_pass}{co.re}")
            print(f"{co.g}[*] username:\t\t\t{co.re}{co.ye}{selected_username}{co.re}")
            print(f"{co.g}[*] password for {selected_username}:\t\t{co.re}{co.ye}{selected_user_pass}{co.re}")
            print(f"{co.g}[*] hostname:\t\t\t{co.re}{co.ye}{selected_hostname}{co.re}")
            print(f"{co.g}[*] aditional packages:\t\t{co.re}{co.ye}{package_list}{co.re}")
            print(f"{co.g}[*] Desktop Enviroment:\t\t{co.re}{co.ye}{selected_DE}{co.re}")
            print(f"{co.re}{co.ye}[*] All settings are saved in the config file.{co.re}")
        else:
            print(f"{co.ye}[!] Command not found ..{co.re}")
    
if __name__ == "__main__":
    teaprompt()
