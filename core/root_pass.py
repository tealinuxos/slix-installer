from core.color import co
import subprocess

### 1.8 set root pass if user input it ###
def set_root_pass(pass_root):
    passwd_input = f"{pass_root}"
    result = subprocess.run(['arch-chroot', '/mnt', 'export', f'$pass="{pass_root}"', '&&', 'echo', '$pass', '|', 'passwd', '--stdin'], input=passwd_input, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode == 0:
        print(f"{co.g}[*] Root password has been set.{co.re}")
    else:
        print(f"{co.r}[!] Error setting root password: {result.stderr}{co.re}")
