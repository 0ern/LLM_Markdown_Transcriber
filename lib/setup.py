import os
import sys
import subprocess
import ctypes

# Initialize Windows Virtual Terminal Processing to enable ANSI color codes
os.system('')

# TERMINAL ANSI COLOR CONFIGURATION CONSTANTS (DARKGRAY THEME)
C_DARKCYAN = "\033[36m"
C_DARKGRAY = "\033[90m"
C_RED = "\033[91m"
C_YELLOW = "\033[93m"
C_GREEN = "\033[92m"
C_RESET = "\033[0m"

try:
    # Attempt to import winreg for Windows registry access
    import winreg
except ImportError:
    pass

def verify_python():
    # Print current system python environment version string
    print(f"{C_DARKGRAY}[1/3] Python Verification: Current version is {sys.version.split()[0]}... [OK]{C_RESET}")

def update_pip():
    # Upgrade pip package manager to the latest version silently
    print(f"{C_DARKGRAY}[2/3] Checking and updating PIP package manager...{C_RESET}")
    try:
        # Run pip upgrade command as a silent background subprocess
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "--upgrade", "pip"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print(f"{C_GREEN}[OK] PIP is updated and ready.{C_RESET}")
    except Exception as e:
        # Catch and report any permission or connection warnings
        print(f"{C_YELLOW}[WARNING] Failed to update PIP globally: {e}{C_RESET}")

def handle_long_paths():
    # Store standard Windows registry target path for path limitation
    print(f"{C_DARKGRAY}[3/3] Checking 'LongPathsEnabled' system configuration...{C_RESET}")
    registry_path = r"SYSTEM\CurrentControlSet\Control\FileSystem"
    
    try:
        # Open the specific registry key with read permissions
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, registry_path, 0, winreg.KEY_READ)
        # Query the specific value of LongPathsEnabled
        value, _ = winreg.QueryValueEx(key, "LongPathsEnabled")
        winreg.CloseKey(key)
        
        # If already set to 1, no further configuration is required
        if value == 1:
            print(f"{C_GREEN}[OK] Long Paths feature is already ENABLED. No action needed.{C_RESET}")
            return
    except Exception:
        pass

    # Warn the user if the feature is disabled
    print(f"{C_YELLOW}[WARNING] Long Paths feature is DISABLED. This may cause CUDA installation failures.{C_RESET}")
    print(f"{C_DARKGRAY}A Windows UAC prompt will appear. Please click 'YES' to authorize.{C_RESET}")
    
    # Define the PowerShell command to force-update the registry entry
    powershell_cmd = r'New-ItemProperty -Path "HKLM:\System\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force'
    
    try:
        # Execute the command with elevated administrative privileges (runas)
        result = ctypes.windll.shell32.ShellExecuteW(
            None, "runas", "powershell.exe", f"-Command {powershell_cmd}", None, 1
        )
        # Check if execution elevation was accepted by the user
        if result > 32:
            print(f"{C_GREEN}[OK] Modification sent to the registry. Restart script if needed.{C_RESET}")
        else:
            print(f"{C_RED}[ERROR] Administrator permission denied by user.{C_RESET}")
    except Exception as e:
        # Handle exceptions during elevation invocation
        print(f"{C_RED}[ERROR] Failed to apply registry patch: {e}{C_RESET}")

if __name__ == "__main__":
    # Main execution wrapper triggering diagnostic functions sequentially
    print(f"{C_DARKGRAY}=== SYSTEM DIAGNOSTICS START ==={C_RESET}")
    verify_python()
    update_pip()
    handle_long_paths()
    print(f"{C_DARKGRAY}=== SYSTEM DIAGNOSTICS END ===\n{C_RESET}")