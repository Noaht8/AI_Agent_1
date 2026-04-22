import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # Will be True or False
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if valid_target_dir == False:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_dir):
            return f'Error: "{file_path}" does not exist or is not a regular file'


        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_dir]

        if args:
            command.extend(args)

        c_p = subprocess.run(command, capture_output=True, text=True, timeout=30, cwd=working_dir_abs)

        output = []
        if c_p.returncode != 0:
            output.append(f"Process exited with code {c_p.returncode}")

        if c_p.stdout == None and c_p.stderr== None:
            output.append("No output produced")

        if c_p.stdout:
            output.append(f"STDOUT: {c_p.stdout}")

        if c_p.stderr:
            output.append(f"STDERR: {c_p.stderr}")

        return "\n".join(output) if output else "No output produced."

    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run python file in a specified directory relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)
