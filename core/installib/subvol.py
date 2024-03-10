import subprocess

def create_subvol():
    subprocess.run("btrfs su cr /mnt/@", shell=True)
    subprocess.run("btrfs su cr /mnt/@home", shell=True)
    subprocess.run("btrfs su cr /mnt/@root", shell=True)
    subprocess.run("btrfs su cr /mnt/@srv", shell=True)
    subprocess.run("btrfs su cr /mnt/@log", shell=True)
    subprocess.run("btrfs su cr /mnt/@cache", shell=True)
    subprocess.run("btrfs su li /mnt", shell=True)
    # Unmounting
    subprocess.run("umount /mnt", shell=True)
        