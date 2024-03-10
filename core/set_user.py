from core.color import co 
import subprocess

### 1.9 set username & pass ###
def set_user_pass(username, user_pass):
    try:
        create_user = subprocess.run(f"arch-chroot /mnt useradd -m -g users -G audio,video,network,wheel,storage,rfkill -s /bin/bash {username}", shell=True, capture_output=True, check=True)
        if create_user.returncode == 0:
            print(f"{co.g}[*] User '{username}' has been created.{co.re}")
        else:
            print(f"{co.r}[!] User '{username}' failed to created.{co.re}")    
        
        create_pass = subprocess.run(f"echo '{user_pass}\n{user_pass}' | arch-chroot /mnt passwd -q {username}", shell=True, check=True, capture_output=True, text=True)
        if "New password: Retype new password: passwd: password updated successfully" in create_pass.stdout:
            print(f"{co.g}[*] User '{username}' has been created with the provided password.{co.re}")
    except subprocess.CalledProcessError as e:
        print(f"{co.r}[!] Error creating user '{username}': {e}{co.re}")
