from core.color import co
import subprocess

### 0.2 partition function ###
def part():
    print("[*] Showing device names:\n")
    lsblk_process = subprocess.run(["lsblk", "--output", "NAME", "--list"], capture_output=True, text=True) ### make the output more readable
    
    # Filter and print only device names
    device_names = []  ### save device in array
    for line in lsblk_process.stdout.split('\n'):
        if line and not line.startswith("NAME"):
            device_name = line.strip()
            device_names.append(device_name)
            print(f"└── /dev/{device_name}") ## output it

    return device_names