import subprocess, os

""" to do list
    help menu: will update
    select language: done
    select time: done
    select keyboard layout: done
 *  setup user: on going
 *  setup desktop environment: on going (gnome, xfce. kde, if u can try add hyprland too)
 *  setup bootloader: on going (for now using grub only)
 *  setup root password: on going
 *  setup audio: on going
 *  setup package: on going
 *  network configuration: on going
 *  setup to connect wifi: on going
 *  setup hostname: on going
**  install tea linix: on going
**  show option: on going (i mean show all configuration that user was do)
    show time zone: done
    show time zone city: done
    clear command: done
    help command: done

"""

### class color ###
class co:
    re = "\33[0m" # reset
    bo = "\33[1m" # bold text
    r = "\33[31m" # red text
    g = "\33[32m" # green text
    ye = "\33[33m" # yellow text

### 0.1 banner  ###
def ban():
    os.system("clear")
    print(f"""{co.g}
               o0xd0x            
            NKkddddddkKN         
         N0xddddddddddddx0N      
      OKxdddddddlodddddddddx0K   
    XOdddddddddd..odddddodddddkX.
   ldddddddddddd. .dddl, oddddddd
   xdddddlddddddo,.d,.   oddddddx
   dddddd..cddddddd.    ;dddddddd    _                         _
   dddddd,   'cdddo   .lddddddddd   | |__  _ __ _____      __ | |_ ___  __ _ 
   ddddddo      'lo :dddddddddddd   | '_ \| '__/ _ \ \ /\ / / | __/ _ \/ _` |
   ddddddd;       ;.ddddddddddddd   | |_) | | |  __/\ V  V /  | ||  __/ (_| |
   dddddddd,       .ddddddddddddd   |_.__/|_|  \___| \_/\_/    \__\___|\__,_|
   oddddddddl'     .ddddddddddddo      ====[ {co.bo}Tea Linux Installer v0.1 {co.re}{co.g}]====
   cdddddddddddc'  .ddddddddddddl
    dddddddddddddo..dddddddddddd 
      :dddddddddddo.dddddddddc   
         ldddddddddcddddddd      
            lddddddddddo         
               .dddd,            
                 ',
    {co.re}""")

### 0.2 partition function ###
def part():
    print("[*] Showing device names:\n")
    lsblk_process = subprocess.run(["lsblk", "--output", "NAME", "--list"], capture_output=True, text=True) ### make the output more readable
    
    # Filter and print only device names
    device_names = []  ### save device in array
    for line in lsblk_process.stdout.split('\n'):
        if line and not line.startswith("NAME"):
            device_name = line.strip()
            device_names.append(device_name)
            print(f"└── /dev/{device_name}") ## output it

    return device_names

### 0.3 selected device, need more impovement to automate make btrfs and for installer  usage ###
def set_device(selected_device, device_names):
    if selected_device in device_names:
        print(f"[*] Selected device set to: {selected_device}")
        return selected_device
    else:
        print("Invalid device name. Please select a valid device.")

### 0.4 set time zone ###
def set_time(region, city):
    subprocess.run(["ln", "-sf", f"/usr/share/zoneinfo/{region}/{city}", "/etc/localtime"]) ## on development i command this line bcz i dont want make my machine get execute this command LOL
    subprocess.run(["hwclock", "--systohc"])
    print(f"[*] Timezone set to {region}/{city}")

### 0.5 show all time zone ###
def list_time_zones():
    print("[*] List of available time zones:\n")
    output = os.popen("ls -l /usr/share/zoneinfo/ | grep '^d' | awk '{print $NF}'").read()
    lines = output.splitlines()
    
    # Organize the output into three columns
    column_width = max(len(line) for line in lines)
    num_columns = 3
    lines_per_column = -(-len(lines) // num_columns)  # Ceiling division

    for i in range(lines_per_column):
        for j in range(num_columns):
            index = i + j * lines_per_column
            if index < len(lines):
                print(f"[*] {lines[index]:<{column_width}}", end="\t")
        print()

### 0.6 show all city in time zone ###
def list_time_city(cityin):
    print(f"[*]  List of available city in {cityin}:\n")
    os.system(f"ls /usr/share/zoneinfo/{cityin}")
    return cityin

### 0.7 set language ###
def list_languages():
    command = "cat /etc/locale.gen | awk '{print $1}'"
    output = os.popen(command).read()
    lines = output.splitlines()

    # Remove comments and leading/trailing whitespaces
    cleaned_lines = [line[1:].strip() for line in lines if line.startswith("#") and line[1:].strip()]

    # Calculate the number of lines per column
    num_columns = 3
    lines_per_column = -(-len(cleaned_lines) // num_columns)  # Ceiling division

    # Print in three columns
    print("\t[*] All language supported by this tool are listed below:")
    for i in range(lines_per_column):
        for j in range(num_columns):
            index = i + j * lines_per_column
            if index < len(cleaned_lines):
                print(f"[*] {cleaned_lines[index]}", end="\t\t\t") # idk i try my best to make the output looks good
        print()

def set_language(locale):
    try:
        # Uncomment the selected language in /etc/locale.gen
        subprocess.run(["sed", "-i", f"s/^#\\s*{locale}/{locale}/", "/etc/locale.gen"])
        # Generate the locale
        subprocess.run(["locale-gen"])
        print(f"[*] Language set to {locale}")

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
    
### 0.7 install arch ###
# need imporve:
# make btrfs the device that user input, and then mount it
# make sure user input package and if not it will be determinate
# and make all logic that will be execute in arch installation
def install_arch(selected_device):
    if selected_device:
        print(f"Installing Arch Linux with Btrfs on /dev/{selected_device}...")
        # (Your installation code here)
    else:
        print("Please set a device using 'set /dev/(device_name)' before installing.")

### install aditional package ###
def install_packages(package_list):
    if package_list:
        print(f"[*] Installing additional packages: {', '.join(package_list)}")
        command = ["pacstrap", "/mnt"]
        command.extend(package_list)
        subprocess.run(command)
        print("[*] Additional packages installed.")
    else:
        print("[*] No additional packages specified.")

### 0.8 show all keymaps ###
def list_keymaps():
    command = "ls /usr/share/kbd/keymaps/**/*.map.gz && ls /usr/share/kbd/keymaps/**/**/*.map.gz"
    try:
        output = subprocess.run(command, shell=True, capture_output=True, text=True)
        keymaps = [line.split("/")[-1].strip().split('.')[0] for line in output.stdout.split('\n') if line]
        return keymaps

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None
    
### 0.8.1 make the output keymaps more better ###
def print_keymaps(keymap_list):
    if keymap_list:
        print("[*] List of available keymaps:\n")
        lines = keymap_list

        # Organize the output into three columns
        column_width = max(len(line) for line in lines)
        num_columns = 3
        lines_per_column = -(-len(lines) // num_columns)  # Ceiling division

        for i in range(lines_per_column):
            for j in range(num_columns):
                index = i + j * lines_per_column
                if index < len(lines):
                    print(f"[*] {lines[index]:<{column_width}}", end="\t")
            print()  # Move to the next line after printing each row

### 0.9 show help ###
def help():
    os.system("clear")
    ban()
    print("""
    Tea Linux Installer Beta Version
    
    options:
    help\t\t\tShow all command
    partition\t\t\tShow all partition on your device
    set (device name)\t\tSetting your device partition to be place for install Tea Linux
    set user\t\t\tMake default user after installation
    set package (package)\tList package that you want install
    set DE\t\t\tSetting your desktop environment
    set time (region) (city)\tSetting localtime
    set language (LocaleCode)\tSetting your /etc/locale.gen
    list time zone\t\tShow all time zone
    list city (region)\t\tShow all city in the region
    list keymaps\t\tShow all keyboard layout
    clear\t\t\tclear prompt
    exit\t\t\tExit installer   
    """)

### 1. main function i think, bcz this the prompt###
def teaprompt():
    selected_device = None
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
        # if user type install
        elif user_input.lower() == 'install':
            install_arch(selected_device, package_list)
        # if user type list time zone
        elif user_input.lower() == 'list time zone':
            list_time_zones()
        # if user type clear
        elif user_input.lower() == 'clear':
            os.system("clear")
            ban()
        # if user type list keymaps
        elif user_input.lower() == 'list keymaps':
            keymap_list = list_keymaps()
            print_keymaps(keymap_list)
        # if user input package that will be installed
        elif user_input.lower().startswith('set package'):
            tokens = user_input.split(' ', 2)
            if len(tokens) == 3:
                _, _, packages = tokens
                package_list = packages.split()
            else:
                print("[!] Invalid 'set package' command format. Please use 'set package Package1 Package2 ...'.")
        # ... (Command lainnya)

        # if user type set time Region City
        elif user_input.lower().startswith('set time'):
            tokens = user_input.split(' ', 3)
            if len(tokens) == 4:
                _, _, region, city = tokens
                set_time(region, city)
            else:
                print("[!] Invalid 'set time' command format. Please use 'set time Region City'.")
                
        # if user type set language
        elif user_input.lower().startswith('set language'):
            tokens = user_input.split(' ', 3)
            if len(tokens) == 2:
                list_languages()
            elif len(tokens) == 3:
                _, _, locale = tokens
                set_language(locale)
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
        else:
            print("[!] Command not found ..")

if __name__ == "__main__":
    teaprompt()
