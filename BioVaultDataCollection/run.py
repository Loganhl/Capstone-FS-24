import subprocess
import threading

def run_script(script):
    try:
        process = subprocess.Popen(['python3.9', script], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # Read the output and errors in real-time
        for line in process.stdout:
            print(f"[{script}] {line.strip()}")
        for line in process.stderr:
            print(f"[{script} ERROR] {line.strip()}")
        process.wait()
    except Exception as e:
        print(f"Error running {script}: {e}")
    finally:
        process.terminate()

def main():
    scripts = ['main.py', 'autoalg.py']
    threads = []

    # Start each script in a separate thread
    for script in scripts:
        thread = threading.Thread(target=run_script, args=(script,))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    print("All scripts have completed.")

if __name__ == "__main__":
    main()
