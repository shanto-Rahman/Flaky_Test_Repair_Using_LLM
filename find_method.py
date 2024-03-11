import sys
import csv

def append_method_to_csv(csv_file_path, method_body):
    with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)

    if not rows:
        print("CSV is empty, no rows to update.")
        return

    # Determine the first empty cell in the last row
    last_row = rows[-1]
    first_empty_cell_index = next((i for i, x in enumerate(last_row) if not x), len(last_row))

    # Update the last row
    if first_empty_cell_index < len(last_row):
        last_row[first_empty_cell_index] = method_body  # Replace the first empty cell
    else:
        last_row.append(method_body)  # Append a new cell if all cells are filled

    # Write the modified content back to the CSV
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows)
 

def find_method_by_line(java_file_path, line_number):
    with open(java_file_path, 'r') as file:
        lines = file.readlines()
        
        # Variables to keep track of parsing state
        method_start_line = None
        brace_stack = []
        
        for i, line in enumerate(lines):
            current_line_number = i + 1
            trimmed_line = line.strip()
            
            # Check for opening brace indicating possible method start or block start
            if '{' in trimmed_line:
                if "class " not in trimmed_line:  # Simple check to avoid class definitions
                    # Potential method start
                    if method_start_line is None:
                        method_start_line = current_line_number
                    brace_stack.append('{')
            
            # Check for closing brace
            if '}' in trimmed_line:
                if brace_stack:
                    brace_stack.pop()
                    if not brace_stack and method_start_line is not None:
                        # End of method found
                        if current_line_number >= line_number >= method_start_line:
                            # The specified line is within the bounds of the current method
                            return ''.join(lines[method_start_line-1:i+1])
                        # Reset for the next method
                        method_start_line = None
        
        return "The specified line is not within a method body, or the method contains complex structures not handled by this approach."


def find_method_by_line_with_flakesync_changes(java_file_path, line_number, threshold, code_from):
    with open(java_file_path, 'r') as file:
        lines = file.readlines()

    # Variables to keep track of parsing state
    method_start_line = None
    brace_stack = []
    modified_method_body = []

    for i, line in enumerate(lines):
        current_line_number = i + 1
        trimmed_line = line.strip()

        # Check for opening brace indicating possible method start or block start
        if '{' in trimmed_line:
            if "class " not in trimmed_line:  # Simple check to avoid class definitions
                # Potential method start
                if method_start_line is None:
                    method_start_line = current_line_number
                brace_stack.append('{')
        
        if method_start_line is not None:
            # Insert the conditional block before the specified line number
            if current_line_number == line_number and code_from == "test_code":
                # Conditional block to insert
                conditional_block = "while (critiPointCount!=true){\n    Thread.yield();\n}\n"
                modified_method_body.append(conditional_block)

            # Append each line to modified method body as it's read
            modified_method_body.append(line)
        
            # Insert the threshold line immediately after the specified line number
            if current_line_number == line_number and code_from == "cut":
                new_line = f"critiPointCount={threshold};\n"  # New line to insert
                modified_method_body.append(new_line)  # Insert the new line

        # Check for closing brace
        if '}' in trimmed_line:
            if brace_stack:
                brace_stack.pop()
                if not brace_stack and method_start_line is not None:
                    # End of method found
                    if current_line_number >= line_number >= method_start_line:
                        # The specified line is within the bounds of the current method
                        # Return the modified method body
                        return ''.join(modified_method_body)
                    else:
                        # Reset for the next method
                        method_start_line = None
                        modified_method_body = []  # Clear the modified method body for the next method

    return "The specified line is not within a method body, or the method contains complex structures not handled by this approach."


if __name__ == "__main__":
    input_file = sys.argv[1]
    line_number = int(sys.argv[2])
    method_body=""
    if len(sys.argv) == 3:
        method_body = find_method_by_line(input_file, line_number)
    else:
        threshold = int(sys.argv[3])
        print(sys.argv)
        code_from = sys.argv[4] #either test code or cut
        #if code_from == "cut":	    
        method_body = find_method_by_line_with_flakesync_changes(input_file, line_number, threshold, code_from) #code_from=cut/ test code
    
    append_method_to_csv('/home/sr53282-admin/Research/Flaky_Test_Repair_Using_LLM/Output.csv', method_body)
    #print(method_body)
