import subprocess

def run_scripts_in_sequence():
    # List of scripts to run in sequence
    script_list = ['p5_deployment_forecast_values.py', 'p6_deployment_metrics.py']
    
    for script in script_list:
        print(f"Running {script} ...")
        try:
            # Run the script
            completed_process = subprocess.run(['python3', script], check=True)
            print(f"{script} completed with return code: {completed_process.returncode}")
        except subprocess.CalledProcessError as e:
            print(f"Error occurred while running {script}: {e}")
            break  # If you want to stop the execution if any script fails

if __name__ == '__main__':
    run_scripts_in_sequence()
