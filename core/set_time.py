from core.color import co
import subprocess

### 0.5 set time zone ###
def set_time(region, city):
    subprocess.run([f"arch-chroot /mnt ln -sf /usr/share/zoneinfo/{region}/{city} /etc/localtime"], shell=True)
    subprocess.run([f"arch-chroot /mnt hwclock --systohc"], shell=True)
    print(f"{co.g}[*] Timezone set to {region}/{city}{co.re}")
    return  region, city