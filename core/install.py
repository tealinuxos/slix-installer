from core.color import co
from core.set_time import set_time
from core.sett_keymap import set_keymap
from core.make_grub import mk_grubb
from core.fstab_check import check_fstab
from core.networkmanager import enable_networkmanager
from core.write_host_file import write_to_hosts_file
from core.install_package import install_packages
from core.set_language import set_language
from core.install_grub import installing_grub
from core.set_hostname import set_hostname
from core.root_pass import set_root_pass
from core.set_user import set_user_pass
from core.install_de import install_desktop_environment
from core.sudoers import update_sudoers
from core.tea_release import update_os_release
from core.installib.format_mount import mount_and_create
from core.installib.subvol import create_subvol
from core.installib.create_dir import create_dirrrr
from core.installib.mount_all_subvol import mount_all_subvol
from core.installib.create_boot_dir import boot_dir
from core.installib.create_and_check_fstab import install_fstab
from core.installib.create_boot_dir import boot_dir

import subprocess, os

def install_tea(selected_device, selected_device_efi, selected_time_region, selected_time_city, selected_lang, selected_keymap, selected_hostname, selected_username, selected_user_pass, selected_root_pass, selected_DE, package_list):
    if selected_device and selected_device_efi:
        print(f"{co.g}Installing Tea Linux with Btrfs on /dev/{selected_device}...{co.re}")
        
        # mounting and format the partition
        mount_and_create(selected_device_efi, selected_device)
        
        # Create subvolumes for root and home
        create_subvol()
        
        # Mounting subvolume
        subprocess.run(f"mount -o defaults,noatime,compress=zstd,commit=120,subvol=@ /dev/{selected_device} /mnt", shell=True)
        
        # Create directories
        create_dirrrr()
        
        # Mounting all subvolumes
        mount_all_subvol(selected_device)
        
        # Create boot directory
        boot_dir(selected_device)
        
        # Install Arch Linux base system
        subprocess.run("pacstrap /mnt base base-devel linux linux-firmware btrfs-progs grub bash wget", shell=True) ## gaada error cuma lupa nganu keyring doang
        # Generate fstab
        install_fstab()
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
        # enabling network manager when i start up
        enable_networkmanager()
        # Change root password
        if selected_root_pass:
            set_root_pass(selected_root_pass)
        else:
            print(f"{co.ye}[!] You not setting root pass ..{co.re}")
        # create boot dir
        boot_dir(selected_device_efi)
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
        if selected_DE:
            install_desktop_environment(selected_DE)
        else:
            print(f"{co.r}[!] Your not choose any Desktop Enviroment .. {co.re}")    
        
        # finish
        print(f"{co.g}[+] Tea Linux was installed ..{co.re}")
        ask = input("Do you want to reboot? [y/N]: ")
        if ask.lower() == "y":
            subprocess.run(["umount -R /mnt"], shell=True)
            print(f"{co.g}[+] umounting /mnt successfully ..{co.re}")
            print(f"{co.g}[+] rebooting system in 5 second ..{co.re}")
            os.system("sleep 5 && reboot")
        else:
            print(f"{co.g}[*] Back to chroot ..{co.re}")
            os.system("arch-chroot /mnt")
        
    else:
        print(f"{co.r}[!] Please set a device using 'set /dev/(device_name)' before installing.{co.re}")
