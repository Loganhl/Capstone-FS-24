import subprocess

def main():
    # Define the script paths
    scripts = [
        'main.py',
        'autoalg.py'
    ]
    
    # Start both scripts using Popen
    processes = []
    try:
        for script in scripts:
            process = subprocess.Popen(['python3.9', script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            processes.append((script, process))
        
        # Monitor processes
        for script, process in processes:
            stdout, stderr = process.communicate()  # This will block for each script in order.
            print(f"Output from {script}:\n{stdout.decode()}")
            if stderr:
                print(f"Errors from {script}:\n{stderr.decode()}")
    
    finally:
        # Ensure all processes are terminated
        for script, process in processes:
            process.terminate()
        print("All processes terminated.")

if __name__ == "__main__":
    main()
