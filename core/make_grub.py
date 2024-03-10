from core.color import co
import subprocess

### 1.1 mkgrub config ###
def mk_grubb():
    try:
        mkgrub = subprocess.run("arch-chroot /mnt grub-mkconfig -o /boot/grub/grub.cfg", shell=True, capture_output=True, text=True)
        if "Found linux image: /boot/vmlinuz-linux" in mkgrub.stderr:
            print(f"{co.g}[*] Grub config was created successfully.{co.re}")
            try:
                with open("/mnt/boot/grub/grub.cfg", 'r') as file:
                    file_content = file.read()
                new_os = file_content.replace("Arch Linux", "Tea Linux")
                with open("/mnt/boot/grub/grub.cfg", 'w') as file:
                    file.write(new_os)
            except Exception as e:
                print(f"{co.r}[!] Error when try change os-release, Error: {e}.{co.re}")
        else:
            print(f"{co.r}[!] Fail while run grub-mkconfig{co.re}")
    except Exception as e:
        print(f"{co.r}Error: {e}{co.re}")