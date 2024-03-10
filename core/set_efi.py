from core.color import co

### 0.4 selected efi device, to install grub ###
def set_device_efi(selected_device_efi, device_names):
    selected_device_efi = selected_device_efi.split('/')[-1]  # Extract the device name
    if selected_device_efi in device_names:
        print(f"[*] Selected EFI device set to: {selected_device_efi}")
        return selected_device_efi
    else:
        print(f"{co.r}[!] Invalid EFI device name. Please select a valid device.{co.re}")
