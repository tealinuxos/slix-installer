from core.color import co
import subprocess

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
