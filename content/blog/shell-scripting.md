+++
title = "Shell Scripting"
description = "Kickstart your automation journey with this beginner-friendly guide to Shell Scripting! Learn how to write powerful shell scripts using basic commands, variables, conditionals, loops, functions, and more. Whether you're printing Hello, World! or handling user input, this guide walks you through the core concepts step by step. Perfect for developers, sysadmins, and curious learners eager to harness the command line."
imagesq = "/images/blog/shell-scripting/shell-scripting-square.webp"
image = "/images/blog/shell-scripting/shell-scripting-thumb.webp"
authorName = "akshat-jain"
date = 2024-01-08T00:00:00+05:30
+++
- Shell scripting is a way to automate tasks by writing scripts (sequences of commands) in a text file, which the shell can execute.

### **Basic Shell Scripting Commands:**

### 1. **`#!/bin/bash`**

- **Purpose:** This is called the *shebang* line. It specifies the interpreter for the script (in this case, Bash). The script will be executed by the Bash shell.
- **Example:** This script will print "Hello, World!" to the screen.
    
    ```bash
    #!/bin/bash
    echo "Hello, World!"
    ```
    

### 2. **`echo`**

- **Purpose:** The `echo` command is used to print a message or the value of a variable to the terminal.
- **Usage :Example:**
    - `echo "Message"` – Prints a string to the terminal.
    - `echo $variable` – Prints the value stored in a variable.
    
    ```bash
    echo "Hello, World!"
    name="Alice"
    echo "Hello, $name"
    ```
    

### 3. **Variables**

- **Purpose:** Variables are used to store data that can be reused later in the script.
- **Usage: Example:**
    - `variable_name="value"` – Declare and assign a value to a variable.
    - `echo $variable_name` – Access the value of a variable.
    
    ```bash
    name="Alice"
    echo "Hello, $name"  # Output: Hello, Alice
    ```
    

### 4. **Conditionals (if/else)**

- **Purpose:** Conditional statements allow the execution of commands based on whether a condition is true or false.
- **Usage:**
    
    ```bash
    if [ condition ]; then
        # command if condition is true
    else
        # command if condition is false
    fi
    
    #!/bin/bash
    
    number=5  # No spaces around '=' in variable assignment
    
    if [ "$number" -eq 5 ]; then
        echo "The number is 5 buddy"
    else
        echo "Teri lowwde"
    fi
    
    ```
    
    **Example:**
    
    ```bash
    if [ $name == "Alice" ]; then
        echo "Hello, Alice!"
    else
        echo "You're not Alice."
    fi
    ```
    
    This checks if the variable `name` is equal to "Alice" and prints a message accordingly.
    

### 5. **Loops (for/while)**

- **Purpose:** Loops allow repeated execution of commands. Useful for iterating over items or performing repetitive tasks.
- **For Loop:**
    
    ```bash
    for i in 1 2 3; do
        echo "Loop $i"
    done
    ```
    
    - This will loop through the numbers 1, 2, and 3, printing each one.
- **While Loop:**
    
    ```bash
    count=1
    while [ $count -le 5 ]; do
        echo "Counter: $count"
        ((count++))
    done
    ```
    
    - This will increment `count` from 1 to 5 and print the value of `count` each time.

### 6. **Reading Input**

- **Purpose:** Accept user input during the execution of a script.
- **Usage:**
    
    ```bash
    read variable_name
    echo "You entered: $variable_name"
    ```
    
    **Example:**
    
    ```bash
    echo "Enter your name:"
    read name
    echo "Hello, $name!"
    ```
    

### 7. **Functions**

- **Purpose:** Functions allow you to group related commands together and reuse them within your script.
- **Usage:**
    
    ```bash
    my_function() {
        echo "This is a function"
    }
    my_function  # Call the function
    ```
    
    **Example:**
    
    ```bash
    greet() {
        echo "Hello, $1!"
    }
    greet "Alice"  # Output: Hello, Alice!
    ```
    
    - `$1` refers to the first argument passed to the function.

### 8. **Making a Script Executable**

- **Purpose:** Allows you to run a script as if it were a command from the terminal.
- **Steps:**
    1. **Make the script executable** using `chmod`:
        
        ```bash
        chmod +x script_name.sh
        ```
        
    2. **Run the script** by calling it directly:
        
        ```bash
        ./script_name.sh
        ```
        
    
    This allows you to execute the script without explicitly invoking the interpreter (e.g., `bash script_name.sh`).
    

### 9. **Comments**

- **Purpose:** Comments are used to explain parts of your script and make it easier to understand.
- **Usage:**
    
    ```bash
    # This is a single-line comment
    ```
    
    **Example:**
    
    ```bash
    # This script greets the user
    echo "Hello, User!"
    ```
    

### 10. **File Redirection and Pipes**

- **Purpose:** Shell scripting allows you to redirect input/output or pipe the output of one command to another.
    - **Redirection:**
        - `>` – Redirects output to a file (overwrites).
        - `>>` – Redirects output to a file (appends).
    - **Pipes:**
        - `|` – Pipes the output of one command to another.
    
    **Examples:**
    
    ```bash
    echo "Hello, World!" > output.txt   # Redirects to a file
    cat output.txt                     # Display the contents of output.txt
    
    ls | grep "file"                   # Pipe the output of ls to grep
    ```
    

### 11. **Exit Status**

- **Purpose:** Every command in a script returns an exit status code, which indicates whether the command was successful.
    - `0` – Success
    - Non-zero – Error
    
    **Usage:**
    
    ```bash
    if [ $? -eq 0 ]; then
        echo "Last command was successful."
    else
        echo "Last command failed."
    fi
    ```