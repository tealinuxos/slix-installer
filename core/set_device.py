from core.color import co

### 0.3 selected device, need more impovement to automate make btrfs and for installer  usage ###
def set_device(selected_device, device_names):
    if selected_device in device_names:
        print(f"[*] Selected device set to: {selected_device}")
        return selected_device
    else:
        print(f"{co.r}[!] Invalid device name. Please select a valid device.{co.re}")
