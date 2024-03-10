from core.color import co
import subprocess

### 1.4 install aditional package from user that input it###
def install_packages(package_list):
    if package_list:
        print(f"{co.g}[*] Installing additional packages: {', '.join(package_list)}{co.re}")
        command = ["pacstrap", "/mnt"]
        command.extend(package_list)
        subprocess.run(command)
        print(f"{co.g}[*] Additional packages successfully installed.{co.re}")
    else:
        print(f"{co.ye}[*] No additional packages specified.{co.re}")
