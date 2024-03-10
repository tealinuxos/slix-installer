from core.color import co
import os

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