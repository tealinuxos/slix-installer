from core.fstab_check import check_fstab
import subprocess

def install_fstab():
    subprocess.run("genfstab -U /mnt >> /mnt/etc/fstab", shell=True) ## done nothing error in here
    check_fstab()
    