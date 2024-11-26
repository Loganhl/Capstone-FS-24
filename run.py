import subprocess

def main():
    # Define the script paths
    scripts = [
        'BioVaultDataCollection/main.py',
        'BioVaultDataCollection/autoalg.py'
    ]
    
    # Start both scripts using Popen
    processes = []
    try:
        for script in scripts:
            process = subprocess.Popen(['python3.9', script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            processes.append(process)
        
        # Wait for the first script (main.py) to finish
        stdout, stderr = processes[0].communicate()
        print(f"Output from {scripts[0]}:\n{stdout.decode()}")
        if stderr:
            print(f"Errors from {scripts[0]}:\n{stderr.decode()}")

        # Let the second script (autoalg.py) continue running as needed
        print(f"{scripts[1]} is still running...")

    finally:
        # Ensure all processes are terminated
        for process in processes:
            process.terminate()
        print("All processes terminated.")

if __name__ == "__main__":
    main()
