from core.color import co 
import subprocess

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
