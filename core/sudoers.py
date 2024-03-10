from core.color import co
import subprocess,re

### 2.1 update file /etc/sudoers to change # wheel....
def update_sudoers():
    # read sudoers
    try:
        result = subprocess.run('arch-chroot /mnt cat /etc/sudoers', shell=True, capture_output=True, text=True)
        sudoers_content = result.stdout.splitlines()
    except FileNotFoundError:
        print(f"{co.r}[!] Error: sudoers file not found.{co.re}")
        return

    # regex pattern to search uncommented wheel
    pattern = r"^# (%wheel\s+ALL=\(ALL:ALL\) ALL)$"
    new_line = "%wheel ALL=(ALL:ALL) ALL"

    updated_content = []
    for line in sudoers_content:
        if re.match(pattern, line.strip()):
            updated_content.append(new_line)  # change the correct line
        else:
            updated_content.append(line)

    updated_sudoers_content = '\n'.join(updated_content)

    # rewrite sudoers
    try:
        with open("/mnt/etc/sudoers", "w") as sudoers_file:
            sudoers_file.write(updated_sudoers_content)
        print(f"{co.g}[*] sudoers file has been updated.{co.re}")
    except PermissionError:
        print(f"{co.r}[!] Error: Permission denied. Make sure you have the necessary permissions to modify the sudoers file.{co.re}")
