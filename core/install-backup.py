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
# from core.installib.format_and_mount import _format_and_mount_device
# from core.installib.create_subvol import _create_subvolumes

import os
import subprocess

class NgetehAsu:
    def __init__(self, selected_device, selected_device_efi, selected_time_region, selected_time_city, selected_lang, selected_keymap, selected_hostname, selected_username, selected_user_pass, selected_root_pass, selected_DE, package_list):
        self.selected_device = selected_device
        self.selected_device_efi = selected_device_efi
        self.selected_time_region = selected_time_region
        self.selected_time_city = selected_time_city
        self.selected_lang = selected_lang
        self.selected_keymap = selected_keymap
        self.selected_hostname = selected_hostname
        self.selected_username = selected_username
        self.selected_user_pass = selected_user_pass
        self.selected_root_pass = selected_root_pass
        self.selected_DE = selected_DE
        self.package_list = package_list

    def _format_and_mount_device(self):
        subprocess.run("pacman -Syy --noconfirm archlinux-keyring", shell=True)
        subprocess.run(f"mkfs.fat -F32 /dev/{self.selected_device_efi}", shell=True)
        subprocess.run(f"mkfs.btrfs -f /dev/{self.selected_device}", shell=True)
        subprocess.run(f"mount /dev/{self.selected_device} /mnt", shell=True)

    def _create_subvolumes(self):
        subprocess.run("btrfs su cr /mnt/@", shell=True)
        subprocess.run("btrfs su cr /mnt/@home", shell=True)
        subprocess.run("btrfs su cr /mnt/@root", shell=True)
        subprocess.run("btrfs su cr /mnt/@srv", shell=True)
        subprocess.run("btrfs su cr /mnt/@log", shell=True)
        subprocess.run("btrfs su cr /mnt/@cache", shell=True)
        subprocess.run("btrfs su cr /mnt/@tmp", shell=True)
        subprocess.run("btrfs su li /mnt", shell=True)

    def _mount_subvolumes(self):
        subprocess.run(f"mount -o defaults,noatime,compress=zstd,commit=120,subvol=@ /dev/{self.selected_device} /mnt", shell=True)
        subprocess.run(f"mount -o defaults,noatime,compress=zstd,commit=120,subvol=@home /dev/{self.selected_device} /mnt/home", shell=True)
        subprocess.run(f"mount -o defaults,noatime,compress=zstd,commit=120,subvol=@root /dev/{self.selected_device} /mnt/root", shell=True)
        subprocess.run(f"mount -o defaults,noatime,compress=zstd,commit=120,subvol=@srv /dev/{self.selected_device} /mnt/srv", shell=True)
        subprocess.run(f"mount -o defaults,noatime,compress=zstd,commit=120,subvol=@log /dev/{self.selected_device} /mnt/var/log", shell=True)
        subprocess.run(f"mount -o defaults,noatime,compress=zstd,commit=120,subvol=@cache /dev/{self.selected_device} /mnt/var/cache", shell=True)
        subprocess.run(f"mount -o defaults,noatime,compress=zstd,commit=120,subvol=@tmp /dev/{self.selected_device} /mnt/tmp", shell=True)

    def _create_boot_directory(self):
        os.system("mkdir -p /mnt/boot/efi")
        subprocess.run(f"mount /dev/{self.selected_device_efi} /mnt/boot/efi", shell=True)

    def install(self):
        if self.selected_device and self.selected_device_efi:
            print(f"{co.g}Installing Tea Linux with Btrfs on /dev/{self.selected_device}...{co.re}")

            # Format and mount the selected device
            self._format_and_mount_device()
            
            # Create subvolumes for root and home
            self._create_subvolumes()
            
            # Unmounting
            subprocess.run("umount /mnt", shell=True)
            
            # Mounting subvolume
            self._mount_subvolumes()
            
            # Create directories
            os.system("mkdir -p /mnt/home")
            os.system("mkdir -p /mnt/root")
            os.system("mkdir -p /mnt/srv")
            os.system("mkdir -p /mnt/tmp")
            os.system("mkdir -p /mnt/var/log")
            os.system("mkdir -p /mnt/var/cache")
            
            # Mounting all subvolumes
            self._mount_subvolumes()
            
            # Create boot directory
            self._create_boot_directory()
            
            # Install Arch Linux base system
            subprocess.run("pacstrap /mnt base base-devel linux linux-firmware btrfs-progs grub bash wget", shell=True)
            # Generate fstab
            subprocess.run("genfstab -U /mnt >> /mnt/etc/fstab", shell=True)
            check_fstab()
            # install additional package
            install_packages(self.package_list)
            # Set time, language, keymap, hostname, hosts
            set_time(self.selected_time_region, self.selected_time_city)
            set_language(self.selected_lang)
            set_keymap(self.selected_keymap)
            set_hostname(self.selected_hostname)
            write_to_hosts_file()
            
            # Install network manager
            os.system("arch-chroot /mnt pacman -S --noconfirm networkmanager grub efibootmgr")
            enable_networkmanager()
            # Change root password
            if self.selected_root_pass:
                set_root_pass(self.selected_root_pass)
            else:
                print(f"{co.ye}[!] You not setting root pass ..{co.re}")
            # Install Grub
            installing_grub()
            # Generate Grub config
            mk_grubb()
            # update os-release
            update_os_release()
            # Create non-root user
            set_user_pass(self.selected_username, self.selected_user_pass)
            # Update sudoers
            update_sudoers()
            # Install desktop environment
            install_desktop_environment(self.selected_DE)
            
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
