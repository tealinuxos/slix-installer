### 1.5.1 make the output keymaps more better ###
def print_keymaps(keymap_list):
    if keymap_list:
        print("[*] List of available keymaps:\n")
        lines = keymap_list

        # Organize the output into three columns
        column_width = max(len(line) for line in lines)
        num_columns = 3
        lines_per_column = -(-len(lines) // num_columns)  # Ceiling division

        for i in range(lines_per_column):
            for j in range(num_columns):
                index = i + j * lines_per_column
                if index < len(lines):
                    print(f"[*] {lines[index]:<{column_width}}", end="\t")
            print()  # Move to the next line after printing each row
