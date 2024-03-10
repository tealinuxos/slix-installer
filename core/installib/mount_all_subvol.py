import subprocess

def mount_all_subvol(selected_device):
    subprocess.run(f"mount -o defaults,noatime,compress=zstd,commit=120,subvol=@home /dev/{selected_device} /mnt/home", shell=True)
    subprocess.run(f"mount -o defaults,noatime,compress=zstd,commit=120,subvol=@root /dev/{selected_device} /mnt/root", shell=True) 
    subprocess.run(f"mount -o defaults,noatime,compress=zstd,commit=120,subvol=@srv /dev/{selected_device} /mnt/srv", shell=True)
    subprocess.run(f"mount -o defaults,noatime,compress=zstd,commit=120,subvol=@log /dev/{selected_device} /mnt/var/log", shell=True)
    subprocess.run(f"mount -o defaults,noatime,compress=zstd,commit=120,subvol=@cache /dev/{selected_device} /mnt/var/cache", shell=True)
        