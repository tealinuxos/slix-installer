import subprocess

def mount_and_create(selected_device_efi, selected_device):
    subprocess.run("pacman -Syy --noconfirm archlinux-keyring", shell=True)
    subprocess.run(f"mkfs.fat -F32 /dev/{selected_device_efi}", shell=True)
    subprocess.run(f"mkfs.btrfs -f /dev/{selected_device}", shell=True)
    subprocess.run(f"mount /dev/{selected_device} /mnt", shell=True)