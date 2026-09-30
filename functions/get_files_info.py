import os

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        abs_work_dir = os.path.abspath(working_directory)
        combined_path = os.path.join(abs_work_dir,directory)
        target_dir = os.path.normpath(combined_path)
        valid_target_dir = os.path.commonpath([target_dir,abs_work_dir]) == abs_work_dir
        
        if not os.path.isdir(target_dir):
            return f"Error: \"{directory}\" is not a directory"
        
        if not valid_target_dir:
            return f"Error: Cannot list \"{directory}\" as it is outside the permitted working directory"
        
        elif valid_target_dir:
            get_info = lambda obj: f"- {obj}: file_size={os.path.getsize(f"{target_dir}/{obj}")} bytes, is_dir={os.path.isdir(f"{target_dir}/{obj}")}"
            return "\n".join(list(map(get_info,os.listdir(target_dir))))
            return f"Success: \"{directory}\" is within the working directory"
        

    
    except Exception as e:
        return f"Error: {e}"