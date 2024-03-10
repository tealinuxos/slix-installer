from core.color import co
import os, subprocess

### 1.2 installing network manager and enable the network manager service ###
def enable_networkmanager():
    os.system("arch-chroot /mnt systemctl start NetworkManager && arch-chroot /mnt systemctl enable NetworkManager")
    check = subprocess.run(["arch-chroot /mnt ls -la /etc/systemd/system/multi-user.target.wants/NetworkManager.service"], shell=True, capture_output=True, text=True) 
    if "/etc/systemd/system/multi-user.target.wants/NetworkManager.service -> /usr/lib/systemd/system/NetworkManager.service" in check.stdout:
        print(f"{co.g}[*] NetworkManager was enabled. {co.re}")
    else:
        print(f"{co.r}[-] NetworkManager doesnt enabled properly. {co.re}")
