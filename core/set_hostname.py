from core.color import co

### 1.7 setting hostname ###
def set_hostname(hostname):
    try:
        with open("/mnt/etc/hostname", "w") as hostnames:
            hostnames.write(hostname)
        
        with open("/mnt/etc/hostname") as hostfile:
            current_hostname = hostfile.read().strip()
            if current_hostname == hostname:
                print(f"{co.g}[*] Hostname was set to {hostname}{co.re}")
            else:
                print(f"{co.r}[-] Setting hostname error.{co.re}")
    except Exception as e:
        print(f"{co.g}Error: {e}{co.re}")
