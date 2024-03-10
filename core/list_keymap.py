import subprocess

### 1.5 show all keymaps ###
def list_keymaps():
    command = "ls /usr/share/kbd/keymaps/**/*.map.gz && ls /usr/share/kbd/keymaps/**/**/*.map.gz"
    try:
        output = subprocess.run(command, shell=True, capture_output=True, text=True)
        keymaps = [line.split("/")[-1].strip().split('.')[0] for line in output.stdout.split('\n') if line]
        return keymaps

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None
