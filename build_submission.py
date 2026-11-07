import os
import zipfile

SOURCE_DIR = "submission"
OUTPUT_ZIP = "submission.zip"

EXCLUDE_NAMES = {
    ".env",
    ".adk",
    "__pycache__",
    ".git",
    ".gitignore",
    "venv",
    "results",
    "data",
    "test_api",
    "Writeup.md",
}

def make_clean_zip():
    if os.path.exists(OUTPUT_ZIP):
        os.remove(OUTPUT_ZIP)

    print(f"[*] Packaging clean '{OUTPUT_ZIP}' from '{SOURCE_DIR}'...")
    count = 0
    with zipfile.ZipFile(OUTPUT_ZIP, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(SOURCE_DIR):
            dirs[:] = [d for d in dirs if d not in EXCLUDE_NAMES and not d.startswith(".")]
            
            for file in files:
                if file in EXCLUDE_NAMES or file.endswith(".pyc") or file.startswith("."):
                    continue
                full_path = os.path.join(root, file)
                # Enforce Linux-compatible forward slashes
                arcname = os.path.relpath(full_path, SOURCE_DIR).replace("\\", "/")
                zf.write(full_path, arcname)
                print(f"  + Added: {arcname}")
                count += 1

    print(f"\n[+] Success! Packaged {count} files cleanly into {OUTPUT_ZIP}.")

if __name__ == "__main__":
    make_clean_zip()