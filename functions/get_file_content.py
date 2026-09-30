import os

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        abs_work_dir = os.path.abspath(working_directory)
        combined_path = os.path.join(abs_work_dir,file_path)
        target_file = os.path.normpath(combined_path)
        valid_target_file = os.path.commonpath([target_file,abs_work_dir]) == abs_work_dir

        if not valid_target_file:
            return f"Error: Cannot read \"{file_path}\" as it is outside the permitted working directory"
        
        if not os.path.isfile(target_file):
            return f"Error: File not found or is not a regular file: \"{file_path}\""
        
        elif valid_target_file:
            MAX_CHARS = 10000
            with open(target_file, "r") as f:
                file_content_string = f.read(MAX_CHARS)
                # After reading the first MAX_CHARS...
                if f.read(1):
                    file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                
                return file_content_string
    
    except Exception as e:
        return f"Error: {e}"