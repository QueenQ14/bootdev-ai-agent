import os

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Write contents into a specified file path relative to the working directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to write content into, relative to the working directory (default is the working directory itself)",
                },
                "content": {
                    "type": "string",
                    "description": "The content that needs to be written into the file.",
                },
            },
            
        },
    },
}

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        abs_work_dir = os.path.abspath(working_directory)
        combined_path = os.path.join(abs_work_dir,file_path)
        target_file = os.path.normpath(combined_path)
        valid_target_file = os.path.commonpath([target_file,abs_work_dir]) == abs_work_dir

        if not valid_target_file:
            return f"Error: Cannot write to \"{file_path}\" as it is outside the permitted working directory"
        
        elif os.path.isdir(target_file):
            return f"Error: Cannot write to \"{file_path}\" as it is a directory"
        
        elif valid_target_file:
            # Create parent directories if they don't exist
            os.makedirs(os.path.dirname(target_file), exist_ok=True)
            with open(target_file, "w") as f:
                f.write(content)
            
            return f"Successfully wrote to \"{file_path}\" ({len(content)} characters written)"
    
    except Exception as e:
        return f"Error: {e}"