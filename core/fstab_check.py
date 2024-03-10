from core.color import co
import os

### check fstab, on development i use this to check if fstab exists or no, usualy no but now its fix ###
def check_fstab():
    fstab_path = "/mnt/etc/fstab"
    if os.path.exists(fstab_path):
        if os.path.getsize(fstab_path) > 0:
            with open(fstab_path, "r") as fstab_file:
                fstab_content = fstab_file.read()
                if "/home" in fstab_content:
                    print(f"{co.g}[*] fstab successfully created{co.re}")
                else:
                    print(f"{co.ye}[-] fstab is empty or error. plis check the code !{co.re}")
        else:
            print(f"{co.ye}[!] fstab exists but empty !{co.re}")
    else:
        print(f"{co.r}[!] fstab doesnt exists check the code !.{co.re}")
