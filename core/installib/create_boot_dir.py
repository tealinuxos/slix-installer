import os,subprocess

def boot_dir(selected_device_efi):
    os.system("mkdir -p /mnt/boot/efi")
    subprocess.run(f"mount /dev/{selected_device_efi} /mnt/boot/efi", shell=True)