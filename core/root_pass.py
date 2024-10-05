from core.color import co
import subprocess

### 1.8 set root pass if user input it ###
def set_root_pass(pass_root):
    try:
        result = subprocess.run(f'echo -e "{pass_root}\n{pass_root}" | passwd root', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            print(f"{co.bo}{co.g}[*] Root password has been set.{co.re}")
        else:
            print(f"{co.r}{co.bo}[!] Error setting root password: {result.stderr}{co.re}")
    except Exception as e:
        print(f"[!] Exception occurred: {e}")
