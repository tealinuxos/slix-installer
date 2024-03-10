from core.color import co
import os 

### 0.6 show all time zone ###
def list_time_zones():
    print("[*] List of available time zones:\n")
    output = os.popen("ls -l /usr/share/zoneinfo/ | grep '^d' | awk '{print $NF}'").read()
    lines = output.splitlines()
    
    # Organize the output into three columns
    column_width = max(len(line) for line in lines)
    num_columns = 3
    lines_per_column = -(-len(lines) // num_columns)  # Ceiling division

    for i in range(lines_per_column):
        for j in range(num_columns):
            index = i + j * lines_per_column
            if index < len(lines):
                print(f"[*] {lines[index]:<{column_width}}", end="\t")
        print()
