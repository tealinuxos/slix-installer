import subprocess, os, re

""" 
code by x0r, this code is nasty anyway
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
   |dddddddddddd. .dddl, odddddd|
   |dddddlddddddo,.d,.   odddddd|
   |ddddd..cddddddd.    ;ddddddd|    _                         _
   |ddddd,   'cdddo   .ldddddddd|   | |__  _ __ _____      __ | |_ ___  __ _ 
   |dddddo      'lo :ddddddddddd|   | '_ \| '__/ _ \ \ /\ / / | __/ _ \/ _` |
   |dddddd;       ;.dddddddddddd|   | |_) | | |  __/\ V  V /  | ||  __/ (_| |
   |ddddddd,       .dddddddddddd|   |_.__/|_|  \___| \_/\_/    \__\___|\__,_|
   |ddddddddl'     .dddddddddddd|      ====[ {co.bo}Tea Linux Installer v0.1 {co.re}{co.g}]====
   |dddddddddddc'  .dddddddddddd|
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
### 0.4 selected efi device, to install grub ###
def set_device_efi(selected_device_efi, device_names):
    selected_device_efi = selected_device_efi.split('/')[-1]  # Extract the device name
    if selected_device_efi in device_names:
        print(f"[*] Selected EFI device set to: {selected_device_efi}")
        return selected_device_efi
    else:
        print(f"{co.r}[!] Invalid EFI device name. Please select a valid device.{co.re}")

### 0.5 set time zone ###
def set_time(region, city):
    subprocess.run([f"arch-chroot /mnt ln -sf /usr/share/zoneinfo/{region}/{city} /etc/localtime"], shell=True)
    subprocess.run([f"arch-chroot /mnt hwclock --systohc"], shell=True)
    print(f"{co.g}[*] Timezone set to {region}/{city}{co.re}")
    return  region, city

### 0.6 show all time zone ###
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

### 0.7 show all city in time zone ###
def list_time_city(cityin):
    print(f"[*]  List of available city in {cityin}:\n")
    os.system(f"ls /usr/share/zoneinfo/{cityin}")
    return cityin

### 0.8 set language ###
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
        subprocess.run([f"arch-chroot /mnt sed -i s/^#\\s*{locale}/{locale}/ /etc/locale.gen"], shell=True)
        # Generate the locale
        subprocess.run([f"arch-chroot /mnt locale-gen"], shell=True)
        subprocess.run([f"arch-chroot /mnt echo LANG={locale} > /etc/locale.conf"], shell=True)
        print(f"{co.g}[*] Language set to {locale}{co.re}")

    except subprocess.CalledProcessError as e:
        print(f"{co.r}Error: {e}{co.re}")
    
### 0.9 install arch ###
# need imporve:
# change grub from arch to tea linux
def install_arch(selected_device, selected_device_efi, selected_time_region, selected_time_city, selected_lang, selected_keymap, selected_hostname, selected_username, selected_user_pass, selected_root_pass, selected_DE, package_list):
    if selected_device and selected_device_efi:
        print(f"{co.g}Installing Tea Linux with Btrfs on /dev/{selected_device}...{co.re}")
        
        # Format and mount the selected device
        subprocess.run("pacman -Syy --noconfirm archlinux-keyring", shell=True)
        subprocess.run(f"mkfs.fat -F32 /dev/{selected_device_efi}", shell=True)
        subprocess.run(f"mkfs.btrfs -f /dev/{selected_device}", shell=True)
        subprocess.run(f"mount /dev/{selected_device} /mnt", shell=True)
        
        # Create subvolumes for root and home
        subprocess.run("btrfs su cr /mnt/@", shell=True)
        subprocess.run("btrfs su cr /mnt/@home", shell=True)
        subprocess.run("btrfs su cr /mnt/@root", shell=True)
        subprocess.run("btrfs su cr /mnt/@srv", shell=True)
        subprocess.run("btrfs su cr /mnt/@log", shell=True)
        subprocess.run("btrfs su cr /mnt/@cache", shell=True)
        subprocess.run("btrfs su cr /mnt/@tmp", shell=True)
        subprocess.run("btrfs su li /mnt", shell=True)
        
        # Unmounting
        subprocess.run("umount /mnt", shell=True)
        
        # Mounting subvolume
        subprocess.run(f"mount -o defaults,noatime,compress=zstd,commit=120,subvol=@ /dev/{selected_device} /mnt", shell=True)
        
        # Create directories
        os.system("mkdir -p /mnt/home")
        os.system("mkdir -p /mnt/root")
        os.system("mkdir -p /mnt/srv")
        os.system("mkdir -p /mnt/tmp")
        os.system("mkdir -p /mnt/var/log")
        os.system("mkdir -p /mnt/var/cache")
        
        # Mounting all subvolumes
        subprocess.run(f"mount -o defaults,noatime,compress=zstd,commit=120,subvol=@home /dev/{selected_device} /mnt/home", shell=True)
        subprocess.run(f"mount -o defaults,noatime,compress=zstd,commit=120,subvol=@root /dev/{selected_device} /mnt/root", shell=True) 
        subprocess.run(f"mount -o defaults,noatime,compress=zstd,commit=120,subvol=@srv /dev/{selected_device} /mnt/srv", shell=True)
        subprocess.run(f"mount -o defaults,noatime,compress=zstd,commit=120,subvol=@log /dev/{selected_device} /mnt/var/log", shell=True)
        subprocess.run(f"mount -o defaults,noatime,compress=zstd,commit=120,subvol=@cache /dev/{selected_device} /mnt/var/cache", shell=True)
        subprocess.run(f"mount -o defaults,noatime,compress=zstd,commit=120,subvol=@tmp /dev/{selected_device} /mnt/tmp", shell=True)
        
        # Create boot directory
        os.system("mkdir -p /mnt/boot/efi")
        subprocess.run(f"mount /dev/{selected_device_efi} /mnt/boot/efi", shell=True)
        
        # Install Arch Linux base system
        subprocess.run("pacstrap /mnt base base-devel linux linux-firmware btrfs-progs grub bash wget", shell=True) ## gaada error cuma lupa nganu keyring doang
        # Generate fstab
        subprocess.run("genfstab -U /mnt >> /mnt/etc/fstab", shell=True) ## done nothing error in here
        check_fstab()
        # install adational package
        install_packages(package_list)
        # Set time, language, keymap, hostname, hosts
        set_time(selected_time_region, selected_time_city)
        set_language(selected_lang)
        set_keymap(selected_keymap)
        set_hostname(selected_hostname)
        write_to_hosts_file()
        
        # Install network manager
        os.system("arch-chroot /mnt pacman -S --noconfirm networkmanager grub efibootmgr")
        enable_networkmanager()
        # Change root password
        if selected_root_pass:
            set_root_pass(selected_root_pass)
        else:
            print(f"{co.ye}[!] You not setting root pass ..{co.re}")
        # Install Grub
        installing_grub()
        # Generate Grub config
        mk_grubb()
        # update os-release
        update_os_release()
        # Create non-root user
        set_user_pass(selected_username, selected_user_pass)
        # Update sudoers
        update_sudoers()
        # Install desktop environment
        install_desktop_environment(selected_DE)
        
        # finish
        print(f"{co.g}[+] Tea Linux was installed ..{co.re}")
        ask = input("Do you want to reboot? [y/N]: ")
        if ask.startswith("y" or "Y"):
            subprocess.run(["umount -R /mnt"], shell=True)
            print(f"{co.g}[+] umounting /mnt successfully ..{co.re}")
            print(f"{co.g}[+] rebooting system in 5 second ..{co.re}")
            os.system("sleep 5 && reboot")
        else:
            print(f"{co.g}[*] Back to chroot ..{co.re}")
            os.system("arch-chroot /mnt")
        
    else:
        print(f"{co.r}[!] Please set a device using 'set /dev/(device_name)' before installing.{co.re}")
### update os-release       
def update_os_release():
    new_content = '''NAME="Tea Linux"
PRETTY_NAME="Tea Linux"
ID=arch
BUILD_ID=rolling
ANSI_COLOR="38;2;23;147;209"
HOME_URL="https://tealinuxos.org/"
DOCUMENTATION_URL="https://tealinuxos.org/dokumentasi/"
LOGO=archlinux-logo'''

    try:
        with open("/mnt/etc/os-release", "w") as file:
            file.write(new_content)
        print(f"{co.g}[*] Updated /etc/os-release successfully.{co.re}")
        os.system("arch-chroot /mnt wget -q https://raw.githubusercontent.com/tealinuxos/brewix-installer/main/neofetch -O /usr/bin/neofetch")
        os.system("arch-chroot /mnt chmod +x /usr/bin/neofetch")
    except Exception as e:
        print(f"{co.r}[!] Error updating /etc/os-release: {e}{co.re}")

### 1. installing grub ###
## need to add some code to change arch to tea linux
def installing_grub():
    try:
        install_grub = subprocess.run("arch-chroot /mnt grub-install --target=x86_64-efi --efi-directory=/boot/efi", shell=True, capture_output=True, text=True)
        if "Installation finished. No error reported" in install_grub.stderr: # idk when i use stdout it return nothing
            print(f"{co.g}[*] Grub successfully installed.{co.re}")
        else:
            print(f"{co.r}[-] Failed installing grub.{co.re}")
            print(f"{co.r}[-] Error message:\n{install_grub.stderr}{co.re}")
    except Exception as e:
        print(f"{co.r}Error: {e}{co.re}")
        
### 1.1 mkgrub config ###
def mk_grubb():
    try:
        mkgrub = subprocess.run("arch-chroot /mnt grub-mkconfig -o /boot/grub/grub.cfg", shell=True, capture_output=True, text=True)
        if "Found linux image: /boot/vmlinuz-linux" in mkgrub.stderr:
            print(f"{co.g}[*] Grub config was created successfully.{co.re}")
            try:
                with open("/mnt/boot/grub/grub.cfg", 'r') as file:
                    file_content = file.read()
                new_os = file_content.replace("Arch Linux", "Tea Linux")
                with open("/mnt/boot/grub/grub.cfg", 'w') as file:
                    file.write(new_os)
            except Exception as e:
                print(f"{co.r}[!] Error when try change os-release, Error: {e}.{co.re}")
        else:
            print(f"{co.r}[!] Fail while run grub-mkconfig{co.re}")
    except Exception as e:
        print(f"{co.r}Error: {e}{co.re}")
        
### check fstab, on development i use this to check if fstab exists or no, usualy no but now its fix ###
def check_fstab():
    fstab_path = "/mnt/etc/fstab"
    if os.path.exists(fstab_path):
        if os.path.getsize(fstab_path) > 0:
            with open(fstab_path, "r") as fstab_file:
                fstab_content = fstab_file.read()
                if "/home" in fstab_content:
                    print(f"{co.g}[*] fstab successfully created{co.re}")
                else:
                    print(f"{co.ye}[-] fstab is empty or error. plis check the code !{co.re}")
        else:
            print(f"{co.ye}[!] fstab exists but empty !{co.re}")
    else:
        print(f"{co.r}[!] fstab doesnt exists check the code !.{co.re}")

### 1.2 installing network manager and enable the network manager service ###
def enable_networkmanager():
    os.system("arch-chroot /mnt systemctl start NetworkManager && arch-chroot /mnt systemctl enable NetworkManager")
    check = subprocess.run(["arch-chroot /mnt ls -la /etc/systemd/system/multi-user.target.wants/NetworkManager.service"], shell=True, capture_output=True, text=True) 
    if "/etc/systemd/system/multi-user.target.wants/NetworkManager.service -> /usr/lib/systemd/system/NetworkManager.service" in check.stdout:
        print(f"{co.g}[*] NetworkManager was enabled. {co.re}")
    else:
        print(f"{co.r}[-] NetworkManager doesnt enabled properly. {co.re}")

### 1.3 add etc/hosts ###
def write_to_hosts_file():
    lines = [
        "127.0.0.1                 localhost",
        "::1                       localhost",
        "127.0.0.1                 tealinux.localdomain"
    ]

    # save the content that will be save in /etc/hosts
    hosts_content = '\n'.join(lines)

    try:
        # open /etc/hosts and add the content
        with open("/mnt/etc/hosts", "a") as hosts_file:
            hosts_file.write(hosts_content + "\n")
        print(f"{co.g}[*] Content has been added to /etc/hosts.{co.re}")
    except Exception as e:
        print(f"{co.r}[!] Error adding content to /etc/hosts: {e}{co.re}")

### 1.4 install aditional package from user that input it###
def install_packages(package_list):
    if package_list:
        print(f"{co.g}[*] Installing additional packages: {', '.join(package_list)}{co.re}")
        command = ["pacstrap", "/mnt"]
        command.extend(package_list)
        subprocess.run(command)
        print(f"{co.g}[*] Additional packages successfully installed.{co.re}")
    else:
        print(f"{co.ye}[*] No additional packages specified.{co.re}")

### 1.5 show all keymaps ###
def list_keymaps():
    command = "ls /usr/share/kbd/keymaps/**/*.map.gz && ls /usr/share/kbd/keymaps/**/**/*.map.gz"
    try:
        output = subprocess.run(command, shell=True, capture_output=True, text=True)
        keymaps = [line.split("/")[-1].strip().split('.')[0] for line in output.stdout.split('\n') if line]
        return keymaps

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None
    
### 1.5.1 make the output keymaps more better ###
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

### 1.6 set keyboard layout ###            
def set_keymap(keymap):
    keymap_list = list_keymaps()
    if keymap in keymap_list:
        try:
            subprocess.run([f"arch-chroot /mnt echo KEYMAP={keymap} > /etc/vconsole.conf"], shell=True)
            print(f"{co.g}[*] Keymap set to {keymap}{co.re}")
        except subprocess.CalledProcessError as e:
            print(f"{co.r}Error: {e}{co.re}")
    else:
        print(f"{co.ye}[!] Invalid keymap code. Please select a valid keymap.{co.re}")

### 1.7 setting hostname ###
def set_hostname(hostname):
    try:
        with open("/mnt/etc/hostname", "w") as hostnames:
            hostnames.write(hostname)
        
        with open("/mnt/etc/hostname") as hostfile:
            current_hostname = hostfile.read().strip()
            if current_hostname == hostname:
                print(f"{co.g}[*] Hostname was set to {hostname}{co.re}")
            else:
                print(f"{co.r}[-] Setting hostname error.{co.re}")
    except Exception as e:
        print(f"{co.g}Error: {e}{co.re}")

### 1.8 set root pass if user input it ###
def set_root_pass(pass_root):
    passwd_input = f"{pass_root}\n{pass_root}\n"
    result = subprocess.run(['arch-chroot', '/mnt', 'passwd'], input=passwd_input.encode(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode == 0:
        print(f"{co.g}[*] Root password has been set.{co.re}")
    else:
        print(f"{co.r}[!] Error setting root password: {result.stderr}{co.re}")
    
### 1.9 set username & pass ###
def set_user_pass(username, user_pass):
    try:
        create_user = subprocess.run(f"arch-chroot /mnt useradd -m -g users -G audio,video,network,wheel,storage,rfkill -s /bin/bash {username}", shell=True, capture_output=True, check=True)
        if create_user.returncode == 0:
            print(f"{co.g}[*] User '{username}' has been created.{co.re}")
        else:
            print(f"{co.r}[!] User '{username}' failed to created.{co.re}")    
        
        create_pass = subprocess.run(f"echo '{user_pass}\n{user_pass}' | arch-chroot /mnt passwd -q {username}", shell=True, check=True, capture_output=True, text=True)
        if "New password: Retype new password: passwd: password updated successfully" in create_pass.stdout:
            print(f"{co.g}[*] User '{username}' has been created with the provided password.{co.re}")
    except subprocess.CalledProcessError as e:
        print(f"{co.r}[!] Error creating user '{username}': {e}{co.re}")

### 2. installing desktop environment that user select ###
## need upgrade to add more desktop environment options ##
def install_desktop_environment(desktop_env):
    if desktop_env.lower() == "gnome":
        subprocess.run(["arch-chroot /mnt pacman -S --noconfirm gnome gnome-tweaks gdm xorg-server xorg-apps xorg-xinit xterm pipewire pipewire-pulse && arch-chroot /mnt systemctl enable gdm -f"], shell=True, check=True) ## error in systemctl start gdm idk in arch chroot got error maybe to the another desktop enviroment is the same one, try to remove systemctl enable gdm start first and run again in pain, bro my internet is really slow that why this take so long
    elif desktop_env.lower() == "xfce":
        subprocess.run(["arch-chroot /mnt pacman -S --noconfirm xfce4 sddm xfce4-goodies xorg-server xorg-apps xorg-xinit xterm pipewire pipewire-pulse && arch-chroot /mnt systemctl enable sddm -f"], shell=True, check=True)
    elif desktop_env.lower() == "kde":
        subprocess.run(["arch-chroot /mnt pacman -S --no-confirm plasma kdm konsole dolphin ark kwrite kcalc spectacle krunner partitionmanager packagekit-qt5 xorg-server xorg-apps xorg-xinit xterm pipewire pipewire-pulse && arch-chroot /mnt systemctl enable kdm -f"], check=True)
    else:
        print(f"{co.ye}Desktop environment '{desktop_env}' is not supported for now.{co.re}")

### 2.1 update file /etc/sudoers to change # wheel....
def update_sudoers():
    # read sudoers
    try:
        result = subprocess.run('arch-chroot /mnt cat /etc/sudoers', shell=True, capture_output=True, text=True)
        sudoers_content = result.stdout.splitlines()
    except FileNotFoundError:
        print(f"{co.r}[!] Error: sudoers file not found.{co.re}")
        return

    # regex pattern to search uncommented wheel
    pattern = r"^# (%wheel\s+ALL=\(ALL:ALL\) ALL)$"
    new_line = "%wheel ALL=(ALL:ALL) ALL"

    updated_content = []
    for line in sudoers_content:
        if re.match(pattern, line.strip()):
            updated_content.append(new_line)  # change the correct line
        else:
            updated_content.append(line)

    updated_sudoers_content = '\n'.join(updated_content)

    # rewrite sudoers
    try:
        with open("/mnt/etc/sudoers", "w") as sudoers_file:
            sudoers_file.write(updated_sudoers_content)
        print(f"{co.g}[*] sudoers file has been updated.{co.re}")
    except PermissionError:
        print(f"{co.r}[!] Error: Permission denied. Make sure you have the necessary permissions to modify the sudoers file.{co.re}")

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
    set keymaps (keymapcode)\tSetting your your keymaps machine
    list time zone\t\tShow all time zone
    list city (region)\t\tShow all city in the region
    list keymaps\t\tShow all keyboard layout
    show options\t\tShow all options that you select
    clear\t\t\tclear prompt
    exit\t\t\tExit installer   
    """)

### 2.3 main function i think, bcz this the prompt###
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
                install_arch(selected_device, selected_device_efi, selected_time_region, selected_time_city, selected_lang, selected_keymap, selected_hostname, selected_username, selected_user_pass, selected_root_pass, selected_DE, package_list)
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
