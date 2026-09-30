import os
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Execute Python file where the file_path is provided, along with optional arguments( this works within the working directory only)",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The file path of the python file that must be executed, it needs to be .py to be a valid extension",
                },
                "args": {
                    "type": "list[str]",
                    "description": "Any additional arguments that need to be passed to the python file that will be executed.",
                },
            },
        },
    },
}

def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    try:
        abs_work_dir = os.path.abspath(working_directory)
        combined_path = os.path.join(abs_work_dir,file_path)
        target_file = os.path.normpath(combined_path)
        valid_target_file = os.path.commonpath([target_file,abs_work_dir]) == abs_work_dir

        if not valid_target_file:
            return f"Error: Cannot execute \"{file_path}\" as it is outside the permitted working directory"
        
        if not os.path.isfile(target_file):
            return f"Error: \"{file_path}\" does not exist or is not a regular file"
        
        if file_path.split(".")[1] != "py":
            print()
            return f"Error: \"{file_path}\" is not a Python file"
        
        command = ["python",target_file]
        if args:
            command.extend(args)
        
        execute = subprocess.run(command, cwd=os.path.dirname(target_file),capture_output=True,text=True,timeout=30)
        output_str = ""
        if execute.returncode != 0:
            output_str += f"Process exited with code {execute.returncode}\n"
        if execute.stdout == '' and execute.stderr == '':
            output_str += "No output produced"
        else:
            output_str += f"STDOUT: {execute.stdout} \n STDERR: {execute.stderr}"
        return output_str
    
    except Exception as e:
        return f"Error: executing Python file: {e}"