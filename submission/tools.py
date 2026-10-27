import os

def read_schema_file(filepath: str) -> str:
    """Reads and returns the text contents of a schema or Python file.

    Args:
        filepath: Relative or absolute path to the file (e.g. 'data/schema.py').
    """
    if not os.path.exists(filepath):
        return f"Error: File '{filepath}' not found."
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

def apply_code_patch(filepath: str, new_content: str) -> str:
    """Overwrites or updates a Python/Schema file with modified source code.

    Args:
        filepath: Target file path to update.
        new_content: The updated Python/Pydantic source code string.
    """
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True) if os.path.dirname(filepath) else None
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        return f"Successfully updated '{filepath}'."
    except Exception as e:
        return f"Error writing patch to file: {str(e)}"