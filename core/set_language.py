from core.color import co
import subprocess

def set_language(locale):
    try:
        # Uncomment the selected language in /etc/locale.gen
        subprocess.run([f"arch-chroot /mnt sed -i s/^#\\s*{locale}/{locale}/ /etc/locale.gen"], shell=True)
        # Generate the locale
        subprocess.run([f"arch-chroot /mnt locale-gen"], shell=True)
        subprocess.run([f"arch-chroot /mnt echo LANG={locale} > /etc/locale.conf"], shell=True)
        print(f"{co.g}[*] Language set to {locale}{co.re}")

    except subprocess.CalledProcessError as e:
        print(f"{co.r}Error: {e}{co.re}")
