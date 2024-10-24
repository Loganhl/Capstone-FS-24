import subprocess
import time

def run_script(script_path):
    try:
        result = subprocess.run(['python', script_path], check=True, capture_output=True, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running {script_path}:\n{e.stderr}")

def main():
    scripts = [
        'newestbio/main.py',
        'AutomatedAlgorithm/autoalg.py'
    ]

    autoalg_process = subprocess.Popen(['python', scripts[1]], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    try:
        run_script(scripts[0])
    finally:
        autoalg_process.terminate()

if __name__ == "__main__":
    main()
