from core.color import co
from core.list_keymap import list_keymaps
import subprocess

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