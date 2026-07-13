import os
import sys
import subprocess

# Terminal ANSI color configuration constants (Matching DARKCYAN/DARKGRAY theme)
C_DARKCYAN = "\033[36m"
C_DARKGRAY = "\033[90m"
C_RED = "\033[91m"
C_YELLOW = "\033[93m"
C_GREEN = "\033[92m"
C_RESET = "\033[0m"

UV_VENV_CLEAR=1

def ensure_environment(lib_dir):
    """
    Automatically downloads uv locally and sets up an isolated virtual environment
    for MarkItDown inside lib/MarkItDown/ ensuring 100% portability.
    """
    # Define the isolated MarkItDown workspace folder path
    markitdown_dir = os.path.join(lib_dir, "MarkItDown")
    os.makedirs(markitdown_dir, exist_ok=True)
    
    # Define paths for the local standalone binaries and environment layout
    bin_dir = os.path.join(markitdown_dir, "bin")
    uv_exe = os.path.join(bin_dir, "uv.exe")
    venv_dir = os.path.join(markitdown_dir, ".venv")
    markitdown_exe = os.path.join(venv_dir, "Scripts", "markitdown.exe")
    
    # Configure strictly local environment variables to prevent global system pollution
    os.environ["UV_CACHE_DIR"] = os.path.join(markitdown_dir, ".uv_cache")
    os.environ["UV_PYTHON_INSTALL_DIR"] = os.path.join(markitdown_dir, ".uv_python")
    os.environ["VIRTUAL_ENV"] = venv_dir  # <-- CORREZIONE: Dice a 'uv' di usare questo venv specifico
    
    # Check if the finalized MarkItDown executable already exists to skip setup
    if not os.path.exists(markitdown_exe):
        print(f"{C_DARKGRAY}[INFO] MarkItDown environment not found. Initiating portable setup...{C_RESET}")
        
        # Step 1: Check and download the 'uv' binary locally if it is missing
        if not os.path.exists(uv_exe):
            print(f"{C_DARKGRAY}[INFO] Local 'uv' manager not found. Downloading via PowerShell...{C_RESET}")
            os.makedirs(bin_dir, exist_ok=True)
            
            # Formulate the isolated PowerShell command to fetch uv without touching system PATH
            ps_command = f"$env:UV_INSTALL_DIR='{bin_dir}'; irm https://astral.sh/uv/install.ps1 | iex"
            try:
                subprocess.run(["powershell", "-Command", ps_command], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except Exception as e:
                print(f"{C_RED}[ERROR] Failed to download 'uv' binary tool: {e}{C_RESET}")
                sys.exit(1)

        # Step 2: Create the dedicated virtual environment using the local uv binary
        print(f"{C_DARKGRAY}[INFO] Creating isolated virtual environment via local 'uv'...{C_RESET}")
        try:
            # Only create a fresh venv if it doesn't exist to prevent Windows folder-locking write errors
            if not os.path.exists(venv_dir):
                subprocess.run([uv_exe, "venv", venv_dir, "--python", sys.executable], check=True, stdout=subprocess.DEVNULL)
            
            # Step 3: Install MarkItDown with all core production document parsers via uv pip
            print(f"{C_DARKGRAY}[INFO] Installing markitdown[all] locally... (This may take a moment){C_RESET}")
            # Use target python-version override to seamlessly bypass strict upper-bound metadata constraints on Python 3.14
            subprocess.run([uv_exe, "pip", "install", "markitdown[all]>=0.1.6", "--python-version", "3.13"], check=True, stdout=subprocess.DEVNULL)
            
            print(f"{C_GREEN}[OK] Standalone MarkItDown environment configured with 100% portability!{C_RESET}\n")
        except Exception as e:
            print(f"{C_RED}[ERROR] Automated 'uv' workspace provisioning failed: {e}{C_RESET}")
            sys.exit(1)

def convert_single_file(file_path, output_dir, lib_dir):
    """
    Converts a single document to markdown using the local MarkItDown executable
    and saves the output to the project's centralized output directory.
    """
    if not os.path.exists(file_path):
        print(f"{C_RED}[ERROR] File not found: {file_path}{C_RESET}")
        return

    # Extract the base file name without extension to build the output .md path
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    output_file_path = os.path.join(output_dir, f"{base_name}.md")
    
    # Resolve the path to the local MarkItDown executable binary
    markitdown_exe = os.path.join(lib_dir, "MarkItDown", ".venv", "Scripts", "markitdown.exe")
    
    print(f"\n{C_DARKCYAN}[CONVERTING] Processing document: {os.path.basename(file_path)}{C_RESET}")
    
    try:
        # Run the MarkItDown executable via python subprocess
        result = subprocess.run([markitdown_exe, file_path, "-o", output_file_path], capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"{C_GREEN}[OK] Successfully converted to: Output_Markdown/{base_name}.md{C_RESET}")
        else:
            print(f"{C_RED}[ERROR] MarkItDown failed to convert file: {result.stderr.strip()}{C_RESET}")
    except Exception as e:
        print(f"{C_RED}[ERROR] Unexpected error during conversion: {e}{C_RESET}")

def process_input_documents_folder(root_dir, output_dir, lib_dir):
    """
    Recursively scans the 'Input_Documents' folder at the root level 
    and converts all discovered document files.
    """
    input_docs_dir = os.path.join(root_dir, "Input_Documents")
    
    # Ensure the directory exists locally (it will be created automatically if missing)
    os.makedirs(input_docs_dir, exist_ok=True)

    # Define standard document extensions compatible with Microsoft MarkItDown parsing
    DOC_EXTENSIONS = ('.pdf', '.docx', '.doc', '.xlsx', '.xls', '.pptx', '.ppt', '.html', '.htm', '.rtf', '.odt', '.ods', '.odp', '.png', '.jpg', '.jpeg')
    
    converted_count = 0
    
    # Walk through the folder layout recursively to look for files
    for root, _, files in os.walk(input_docs_dir):
        for file in files:
            if file.lower().endswith(DOC_EXTENSIONS):
                full_file_path = os.path.join(root, file)
                convert_single_file(full_file_path, output_dir, lib_dir)
                converted_count += 1
                
    if converted_count == 0:
        print(f"{C_YELLOW}[INFO] No supported document files found inside 'Input_Documents'.{C_RESET}")
    else:
        print(f"\n{C_GREEN}[SUCCESS] Finished batch conversion! Processed {converted_count} document(s).{C_RESET}")