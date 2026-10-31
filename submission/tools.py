import os
import glob
import py_compile

def read_schema_file(filepath: str) -> str:
    """Reads and returns the contents of a file on disk."""
    if not os.path.exists(filepath):
        return f"Error: File not found at path '{filepath}'."
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file '{filepath}': {str(e)}"

def search_repo_files(pattern: str) -> str:
    """Finds files matching a glob pattern such as '**/*.py'. Locates source files when exact path is unknown."""
    try:
        matches = glob.glob(pattern, recursive=True)
        if not matches:
            return f"No files matching pattern '{pattern}' found."
        return "\n".join(matches[:25])
    except Exception as e:
        return f"Error searching files with pattern '{pattern}': {str(e)}"

def grep_code(keyword: str) -> str:
    """Searches for a specific keyword or symbol across Python files in the directory."""
    results = []
    try:
        files = glob.glob("**/*.py", recursive=True)
        for filepath in files[:40]:
            if os.path.isfile(filepath):
                try:
                    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                        for line_no, line in enumerate(f, 1):
                            if keyword in line:
                                results.append(f"{filepath}:{line_no}: {line.strip()[:100]}")
                                if len(results) >= 20:
                                    return "\n".join(results)
                except Exception:
                    continue
        return "\n".join(results) if results else f"Keyword '{keyword}' not found in python files."
    except Exception as e:
        return f"Error searching keyword '{keyword}': {str(e)}"

def apply_code_patch(filepath: str, patch_content: str) -> str:
    """Writes updated code content directly to the target file and verifies Python syntax."""
    try:
        if os.path.dirname(filepath):
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(patch_content)
        
        if filepath.endswith(".py"):
            try:
                py_compile.compile(filepath, doraise=True)
            except py_compile.PyCompileError as compile_err:
                return f"Patch written, but SYNTAX CHECK FAILED: {str(compile_err)}. Please inspect and fix."

        return f"Successfully applied patch to '{filepath}' and verified syntax."
    except Exception as e:
        return f"Error applying patch to '{filepath}': {str(e)}"