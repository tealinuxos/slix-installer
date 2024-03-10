from core.color import co
import os

### 0.8 set language ###
def list_languages():
    command = "cat /etc/locale.gen | awk '{print $1}'"
    output = os.popen(command).read()
    lines = output.splitlines()

    # Remove comments and leading/trailing whitespaces
    cleaned_lines = [line[1:].strip() for line in lines if line.startswith("#") and line[1:].strip()]

    # Calculate the number of lines per column
    num_columns = 3
    lines_per_column = -(-len(cleaned_lines) // num_columns)  # Ceiling division

    # Print in three columns
    print("\t[*] All language supported by this tool are listed below:")
    for i in range(lines_per_column):
        for j in range(num_columns):
            index = i + j * lines_per_column
            if index < len(cleaned_lines):
                print(f"[*] {cleaned_lines[index]}", end="\t\t\t") # idk i try my best to make the output looks good
        print()
