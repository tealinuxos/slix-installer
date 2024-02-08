import subprocess, os, re

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
        print(f"{co.r}[!] Invalid device name. Please select a valid device.{co.re}")

def set_device_efi(selected_device_efi, device_names):
    selected_device_efi = selected_device_efi.split('/')[-1]  # Extract the device name
    if selected_device_efi in device_names:
        print(f"[*] Selected EFI device set to: {selected_device_efi}")
        return selected_device_efi
    else:
        print(f"{co.r}[!] Invalid EFI device name. Please select a valid device.{co.re}")

### 0.4 set time zone ###
def set_time(region, city):
    subprocess.run(["ln", "-sf", f"/usr/share/zoneinfo/{region}/{city}", "/etc/localtime"]) ## on development i command this line bcz i dont want make my machine get execute this command LOL
    subprocess.run(["hwclock", "--systohc"])
    print(f"[*] Timezone set to {region}/{city}")
    return  region, city

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
        subprocess.run(["echo", f"LANG={locale}", ">", "/etc/locale.conf"])
        print(f"[*] Language set to {locale}")

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
    
### 0.7 install arch ###
# need imporve:
# make btrfs the device that user input, and then mount it
# make sure user input package and if not it will be determinate
# and make all logic that will be execute in arch installation
def install_arch(selected_device,selected_device_efi,selected_time_region,selected_time_city,selected_lang, selected_keymap,selected_hostname, selected_username, selected_user_pass, selected_root_pass,selected_DE):
    if selected_device and selected_device_efi:
        print(f"{co.g}Installing Arch Linux with Btrfs on /dev/{selected_device}...{co.re}")
        # Format and mount the selected device
        subprocess.run(["mkfs.btrfs", f"/dev/{selected_device}"])
        subprocess.run(["mount", f"/dev/{selected_device}", "/mnt"])

        # Create subvolumes for root and home
        subprocess.run(["btrfs", "su", "cr", "/mnt/@"])
        subprocess.run(["btrfs", "su", "cr", "/mnt/@home"])
        subprocess.run(["btrfs", "su", "cr", "/mnt/@root"])
        subprocess.run(["btrfs", "su", "cr", "/mnt/@srv"])
        subprocess.run(["btrfs", "su", "cr", "/mnt/@log"])
        subprocess.run(["btrfs", "su", "cr", "/mnt/@cache"])
        subprocess.run(["btrfs", "su", "cr", "/mnt/@tmp"])
        subprocess.run(["btrfs", "su", "li", "/mnt"])
        
        # umounting
        subprocess.run(["cd", "/"])
        subprocess.run(["umount", "/mnt"])
        
        # mounting subvolume
        subprocess.run(["mount", "-o", "defaus,noatime,compress=zstd,commit=120,subvol=@", f"/dev/{selected_device}", "/mnt"])

        # make dir
        os.system("mkdir -p /mnt/home")
        os.system("mkdir -p /mnt/root")
        os.system("mkdir -p /mnt/srv")
        os.system("mkdir -p /mnt/tmp")
        os.system("mkdir -p /mnt/var/log")
        os.system("mkdir -p /mnt/var/cache")

        # mounting all subvolume
        subprocess.run(["mount", "-o", "defaus,noatime,compress=zstd,commit=120,subvol=@home", f"/dev/{selected_device}", "/mnt/home"])
        subprocess.run(["mount", "-o", "defaus,noatime,compress=zstd,commit=120,subvol=@root", f"/dev/{selected_device}", "/mnt/root"]) 
        subprocess.run(["mount", "-o", "defaus,noatime,compress=zstd,commit=120,subvol=@srv", f"/dev/{selected_device}", "/mnt/srv"])
        subprocess.run(["mount", "-o", "defaus,noatime,compress=zstd,commit=120,subvol=@log", f"/dev/{selected_device}", "/mnt/var/log"])
        subprocess.run(["mount", "-o", "defaus,noatime,compress=zstd,commit=120,subvol=@cache", f"/dev/{selected_device}", "/mnt/var/cache"])
        subprocess.run(["mount", "-o", "defaus,noatime,compress=zstd,commit=120,subvol=@tmp", f"/dev/{selected_device}", "/mnt/tmp"])

        # make dir boot
        os.system("mkdir -p /mnt/boot/efi")
        subprocess.run(["mount", f"/dev/{selected_device_efi}", "mnt/boot/efi"])

        # Install Arch Linux base system
        subprocess.run(["pacstrap", "/mnt", "base", "base-devel", "linux", "linux-firmware", "btrfs-progs", "grub"])
        
        # genfstab
        subprocess.run(["genfstab", "-U", "/mnt", ">>", "/mnt/etc/fstab"])
        
        # arch chroot !!
        subprocess.run(["arch-chroot", "/mnt"])
        
        # setting time
        set_time(selected_time_region, selected_time_city)
        # setting language
        set_language(selected_lang)
        # setting keymaps
        set_keymap(selected_keymap)
        # setting hostname
        set_hostname(selected_hostname)
        # setting hosts
        write_to_hosts_file()
        # install network manager
        os.system("pacman -S --noconfirm networkmanager grub efibootmgr && systemctl enable NetworkManager")
        # change root pass
        if selected_root_pass:
            set_root_pass(selected_root_pass)
        else:
            pass
        # Install Grub
        install_grub = subprocess.run(["grub-install", "--target=x86_64-efi", "--efi-directory=/boot/efi"], capture_output=True, text=True)
        # Check if installation finished without error
        if install_grub.returncode == 0 and "Installation finished. No error reported." in install_grub.stdout:
            print(f"{co.g}[*] Install Grub Finished{co.re}")
        else:
            print(f"{co.g}[-] Grub installation failed. Please check for errors.{co.re}")
        # grub mkconfig
        mkgrub = subprocess.run(["grub-mkconfig", "-O", "/boot/grub/grub.cfg"], capture_output=True, text=True)
        if mkgrub == 0 and "Found linux image:" and "Found initrd image:" and "Found fallback initrd image(s) in /boot:" in mkgrub.stdout:
            print(f"{co.g}[*] Grub config was created successfully.{co.re}")
        else:
            print(f"{co.g}[-] Grub config failed to install ...{co.re}")
        # created non root user
        set_user_pass(selected_username, selected_user_pass)
        # update sudoers
        update_sudoers()
        # install DE
        install_desktop_environment(selected_DE)

    else:
        print("Please set a device using 'set /dev/(device_name)' before installing.")

def write_to_hosts_file():
    lines = [
        "# Static table lookup for hostnames.",
        "# See hosts(5) for details.",
        "127.0.0.1                 localhost",
        "::1                       localhost",
        "127.0.0.1                 tealinux.localdomain"
    ]

    with open("/etc/hosts", "a") as file:
        for line in lines:
            file.write(line + "\n")

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
      
            
def set_keymap(keymap):
    keymap_list = list_keymaps()
    if keymap in keymap_list:
        try:
            subprocess.run(["echo", f"KEYMAP={keymap}", ">", "/etc/vconsole.conf"])
            print(f"[*] Keymap set to {keymap}")
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
    else:
        print("[!] Invalid keymap code. Please select a valid keymap.")

def set_hostname(hostname):
        try:
            subprocess.run(["echo", f"{hostname}", ">", "/etc/hostname"])
            print(f"[*] Hostname was set to {hostname}")
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")

### set root pass ###
def set_root_pass(pass_root):
    result = subprocess.run(['passwd'], input=pass_root.encode(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, text=True)
    if result.returncode == 0:
        print("[*] Root password has been set.")
    else:
        print("[!] Error setting root password:", result.stderr)
    
### set username & pass ###
def set_user_pass(username, user_pass):
    try:
        subprocess.run(["useradd", "-m", "-g", "users", "-G", "audio,video,network,wheel,storage,rfkill", "-s", "/bin/bash", username], check=True)
        subprocess.run(["passwd", username], input=user_pass.encode(), check=True)
        print(f"[*] User '{username}' has been created with the provided password.")
    except subprocess.CalledProcessError as e:
        print(f"[!] Error creating user '{username}': {e}")

def install_desktop_environment(desktop_env):
    if desktop_env.lower() == "gnome":
        subprocess.run(["pacman", "-S", "--noconfirm", "gnome", "gnome-tweaks", "gdm", "xorg-server", "xorg-apps", "xorg-xinit", "xterm", "&&", "systemctl", "start", "gdm.service", "&&", "systemctl", "enable", "gdm.service", "-f"], check=True)
    elif desktop_env.lower() == "xfce":
        subprocess.run(["pacman", "-S", "xfce4", "sddm", "xfce4-goodies", "xorg-server", "xorg-apps", "xorg-xinit", "xterm", "&&", "systemctl", "start", "sddm.service", "&&", "systemctl", "enable", "sddm.service", "-f"], check=True)
    elif desktop_env.lower() == "kde":
        subprocess.run(["pacman", "-S", "--no-confirm", "plasma", "kdm", "konsole", "dolphin", "ark", "kwrite kcalc", "spectacle", "krunner", "partitionmanager", "packagekit-qt5", "xorg-server", "xorg-apps", "xorg-xinit", "xterm",  "&&", "systemctl", "start", "kdm.service", "&&", "systemctl", "enable", "kdm.service", "-f"], check=True)
    else:
        print(f"Desktop environment '{desktop_env}' is not supported.")

def update_sudoers():
    # read sudoers
    try:
        with open("/etc/sudoers", "r") as file:
            sudoers_content = file.readlines()
    except FileNotFoundError:
        print(f"{co.r}[!] Error: sudoers file not found.{co.re}")
        return

    # regex wheel 
    pattern = r"^# (%wheel\s+ALL=\(ALL:ALL\) ALL)$"
    new_line = "%wheel ALL=(ALL:ALL) ALL"

    updated_content = []
    for line in sudoers_content:
        if re.match(pattern, line.strip()):
            updated_content.append(new_line + "\n")  # change the # %wheel ALL=(ALL:ALL) ALL
        else:
            updated_content.append(line)

    # rewrite sudoers
    try:
        with open("/etc/sudoers", "w") as file:
            file.writelines(updated_content)
        print(f"{co.g}[*] sudoers file has been updated.{co.re}")
    except PermissionError:
        print(f"{co.r}[!] Error: Permission denied. Make sure you have the necessary permissions to modify the sudoers file.{co.re}")
        

### 0.9 show help ###
def help():
    os.system("clear")
    ban()
    print("""
    Tea Linux Installer Beta Version
    
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
    set keymaps (keymapcode)\tSetting your your keymaps machine
    list time zone\t\tShow all time zone
    list city (region)\t\tShow all city in the region
    list keymaps\t\tShow all keyboard layout
    show options\t\tShow all options that you select
    clear\t\t\tclear prompt
    exit\t\t\tExit installer   
    """)

### 1. main function i think, bcz this the prompt###
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
                install_arch(selected_device, package_list, selected_device_efi, selected_time_city, selected_time_region, selected_lang, selected_keymap,selected_hostname, selected_root_pass,selected_user_pass,selected_username,package_list, selected_DE)
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
            
        
        elif user_input.lower().startswith('set keymaps'):
            tokens = user_input.split(' ', 3)
            if len(tokens) == 3:
                _, _, keymap = tokens
                selected_keymap = keymap
                keymap_list = list_keymaps()
                if keymap in keymap_list:
                    print(f"{co.g}[*] Keymap set to {selected_keymap}{co.re}")
                else:
                    print("[!] Invalid keymap code. Please select a valid keymap.")
            else:
                print("[!] Invalid 'set keymap' command format. Please use 'set keymap keymap_code'.")
            
            # if user input package that will be installed
        elif user_input.lower().startswith('set package'):
            tokens = user_input.split(' ', 2)
            if len(tokens) == 3:
                _, _, packages = tokens
                package_list = packages.split()
                print(f"[*] Package that will be install : {', '.join(package_list)}")
            else:
                print("[!] Invalid 'set package' command format. Please use 'set package Package1 Package2 ...'.")

        # if user type set time Region City
        elif user_input.lower().startswith('set time'):
            tokens = user_input.split(' ', 3)
            if len(tokens) == 4:
                _, _, region, city = tokens
                selected_time_region = region
                selected_time_city = city
                print(f"{co.g}[*] Time set to {region}/{city} ..{co.re}")
            else:
                print("[!] Invalid 'set time' command format. Please use 'set time Region City'.")
                
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
                
        elif user_input.lower().startswith('set hostname'):
            tokens = user_input.split(' ', 3)
            if len(tokens) == 3:
                _, _, hostname = tokens
                selected_hostname = hostname
                print(f"{co.g}[*] Hostname set to {selected_hostname}{co.re}")
            else:
                print("[!] Invalid 'set hostname' command format. Please use 'set hostname YourHostName'.")
        
        elif user_input.lower().startswith('show options'):
            print(f"{co.g}[*] partition for Tea install:\t{selected_device}")
            print(f"[*] partition for EFI:\t\t{selected_device_efi}")
            print(f"[*] region time:\t\t{selected_time_region}")
            print(f"[*] city time:\t\t\t{selected_time_city}")
            print(f"[*] language:\t\t\t{selected_lang}")
            print(f"[*] keymaps:\t\t\t{selected_keymap}")
            print(f"[*] root password:\t\t{selected_root_pass}")
            print(f"[*] username:\t\t\t{selected_username}")
            print(f"[*] password for {selected_username}:\t\t{selected_user_pass}")
            print(f"[*] hostname:\t\t\t{selected_hostname}")
            print(f"[*] aditional packages:\t\t{package_list}")
            print(f"[*] Desktop Enviroment:\t\t{selected_DE}")
            print(f"{co.re}{co.ye}[*] All settings are saved in the config file.{co.re}")
        else:
            print("[!] Command not found ..")
    
if __name__ == "__main__":
    teaprompt()
