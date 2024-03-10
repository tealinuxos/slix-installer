from core.color import co

### 1.3 add etc/hosts ###
def write_to_hosts_file():
    lines = [
        "127.0.0.1                 localhost",
        "::1                       localhost",
        "127.0.0.1                 tealinux.localdomain"
    ]

    # save the content that will be save in /etc/hosts
    hosts_content = '\n'.join(lines)

    try:
        # open /etc/hosts and add the content
        with open("/mnt/etc/hosts", "a") as hosts_file:
            hosts_file.write(hosts_content + "\n")
        print(f"{co.g}[*] Content has been added to /etc/hosts.{co.re}")
    except Exception as e:
        print(f"{co.r}[!] Error adding content to /etc/hosts: {e}{co.re}")