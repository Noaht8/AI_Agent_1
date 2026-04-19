import os

def write_file(working_directory, file_path, content):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # Will be True or False
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if valid_target_dir == False:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(target_dir):
            return f'Error: Cannot write to "{file_path}" as it is a directory'


        

        # Ensure the directory for the file exists
        dir_name = os.path.dirname(file_path)
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name, exist_ok=True)

        # Create the file if it doesn't exist
        if not os.path.exists(file_path):
            with open(target_dir, "w") as f:
                f.write("")  # create empty file

        with open(target_dir, 'w') as f:
            f.write(content)
        
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'






    except Exception as e:
        return f"Error: {e}"
