import sys

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

if __name__ == "__main__":
    input_file = sys.argv[1]
    line_number = int(sys.argv[2])
    method_body = find_method_by_line(input_file, line_number)
    print(method_body)
